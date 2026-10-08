"""The factory builds a Calculation from a name; it never runs the math."""

import pytest

from calculator.calculation import Calculation
from calculator.factory import CalculationFactory
from calculator.operations import Operations


def test_create_returns_a_calculation_not_a_number():
    calculation = CalculationFactory.create("add", 2, 3)
    assert isinstance(calculation, Calculation)
    assert calculation.operation is Operations.add
    assert calculation.get_result() == 5.0


def test_name_is_cleaned_up_before_lookup():
    calculation = CalculationFactory.create(" ADD ", "2", "3")
    assert calculation.get_result() == 5.0


def test_each_name_selects_its_operation():
    assert CalculationFactory.create("subtract", 10, 4).get_result() == 6.0
    assert CalculationFactory.create("multiply", 3, 4).get_result() == 12.0
    assert CalculationFactory.create("divide", 7, 2).get_result() == 3.5


def test_unknown_name_fails_inside_create():
    # Reported during creation: no Calculation is ever built.
    with pytest.raises(ValueError, match="Unknown operation: pizza"):
        CalculationFactory.create("pizza", 2, 3)


def test_zero_division_fails_only_in_get_result():
    # Creation succeeds, which proves create never runs the math...
    calculation = CalculationFactory.create("divide", 1, 0)
    assert isinstance(calculation, Calculation)
    # ...the error only appears when the caller asks for the result.
    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


# Part 3: one, two, or many values, plus named settings

def test_create_one_value_operations():
    assert CalculationFactory.create("square", 3).get_result() == 9.0
    assert CalculationFactory.create("sqrt", 9).get_result() == 3.0


def test_create_sum_with_many_values():
    assert CalculationFactory.create("sum", 2, 3, 4).get_result() == 9.0
    values = ["1", "2", "3", "4"]
    assert CalculationFactory.create("sum", *values).get_result() == 10.0


def test_create_power_with_and_without_exponent():
    values = [3]
    options = {"exponent": 4}
    calculation = CalculationFactory.create("power", *values, **options)
    assert calculation.get_result() == 81.0
    assert CalculationFactory.create("power", 5).get_result() == 25.0


def test_exponent_text_is_converted_to_a_number():
    calculation = CalculationFactory.create("power", 3, exponent="4")
    assert calculation.options == {"exponent": 4.0}


@pytest.mark.parametrize("name, values", [
    ("add", (1,)),
    ("add", (1, 2, 3)),
    ("square", ()),
    ("sqrt", (4, 9)),
    ("power", (2, 3)),
])
def test_wrong_number_of_values_is_rejected(name, values):
    with pytest.raises(ValueError, match="requires exactly"):
        CalculationFactory.create(name, *values)


def test_sum_with_no_values_fails_when_executed():
    calculation = CalculationFactory.create("sum")
    with pytest.raises(ValueError, match="at least one"):
        calculation.get_result()


def test_unsupported_setting_is_rejected():
    with pytest.raises(ValueError, match="Unsupported option for add: exponent"):
        CalculationFactory.create("add", 1, 2, exponent=2)


def test_nonnumeric_setting_is_rejected():
    with pytest.raises(ValueError, match="numeric"):
        CalculationFactory.create("power", 2, exponent="big")


def test_negative_sqrt_builds_then_fails_during_execution():
    calculation = CalculationFactory.create("sqrt", -4)
    with pytest.raises(ValueError):
        calculation.get_result()