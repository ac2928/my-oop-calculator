"""A factory centralizes construction; it does not execute math."""

from calculator.calculation import Calculation
from calculator.operations import Operations
from calculator.validation import numeric_values


class CalculationFactory:
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
        "square": Operations.square,
        "sqrt": Operations.sqrt,
        "power": Operations.power,
        "sum": Operations.sum,
        "mean": Operations.mean,
        "stddev": Operations.stddev,
    }

    # How many values each fixed-size operation needs.
    # sum, mean, and stddev are not listed: they take many values and
    # check their own minimum.
    operand_counts = {
        "add": 2,
        "subtract": 2,
        "multiply": 2,
        "divide": 2,
        "square": 1,
        "sqrt": 1,
        "power": 1,
    }

    # Which named settings each operation accepts.
    allowed_options = {
        "power": {"exponent"},
        "stddev": {"ddof"},
    }

    @staticmethod
    def create(name, *values, **options):
        name = name.strip().lower()
        try:
            operation = CalculationFactory.operations[name]
        except KeyError:
            raise ValueError(f"Unknown operation: {name}") from None

        allowed = CalculationFactory.allowed_options.get(name, set())
        settings = {}
        for key, value in options.items():
            if key not in allowed:
                raise ValueError(f"Unsupported option for {name}: {key}")
            settings[key] = numeric_values([value])[0]

        count = CalculationFactory.operand_counts.get(name)
        if count is not None and len(values) != count:
            raise ValueError(f"{name} requires exactly {count} value(s).")

        return Calculation(values, operation, **settings)