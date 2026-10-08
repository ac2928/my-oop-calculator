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