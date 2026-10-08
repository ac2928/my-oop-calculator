"""Calculation stores values, settings, and a callable; get_result runs it."""

import pytest

from calculator.calculation import Calculation
from calculator.operations import Operations


def test_add():
    calculation = Calculation((10, 5), Operations.add)
    assert calculation.get_result() == 15


def test_instances_have_their_own_operands():
    first = Calculation((10, 5), Operations.add)
    second = Calculation((100, 50), Operations.add)
    first.values = (20.0, 5.0)
    assert first.get_result() == 25
    assert second.values == (100, 50)
    assert second.get_result() == 150


def test_negative_operand():
    assert Calculation((-10, 5), Operations.add).get_result() == -5


def test_zero_operands():
    assert Calculation((0, 0), Operations.add).get_result() == 0


def test_subtract():
    assert Calculation((20, 7), Operations.subtract).get_result() == 13


def test_subtract_can_return_a_negative_result():
    assert Calculation((5, 10), Operations.subtract).get_result() == -5


def test_construction_does_not_call_math():
    # Spy test from the lesson: construction stores the function but does not run it.
    calls = []

    def spy_add(a, b):
        calls.append((a, b))
        return a + b

    calculation = Calculation((2, 3), spy_add)
    assert calls == []                     # nothing ran during construction
    assert calculation.get_result() == 5
    assert calls == [(2.0, 3.0)]           # exactly one call, in get_result


def test_one_class_holds_different_operations():
    calculations = [
        Calculation((10, 5), Operations.add),
        Calculation((20, 7), Operations.subtract),
    ]
    results = []
    for calculation in calculations:
        results.append(calculation.get_result())
    assert results == [15, 13]


def test_zero_divisor_constructs_then_fails_during_execution():
    calculation = Calculation((1, 0), Operations.divide)
    with pytest.raises(ZeroDivisionError):
        calculation.get_result()


# My own tests

def test_add_positive_and_negative_operands_preserves_state():
    calc = Calculation((15, -7), Operations.add)
    result = calc.get_result()
    assert result == 8
    assert calc.values == (15, -7)


def test_polymorphism_with_three():
    calculations = [
        Calculation((4, 6), Operations.add),
        Calculation((3, 10), Operations.subtract),
        Calculation((2, 5), Operations.add),
    ]
    results = []
    for calculation in calculations:
        results.append(calculation.get_result())
    assert results == [10, -7, 7]


def test_decimal_addition():
    assert Calculation((0.1, 0.2), Operations.add).get_result() == pytest.approx(0.3)


def test_decimal_subtraction():
    assert Calculation((1.5, 0.25), Operations.subtract).get_result() == 1.25


def test_subtract_two_negative_operands():
    assert Calculation((-10, -5), Operations.subtract).get_result() == -5


def test_subtract_zero_operands():
    assert Calculation((0, 0), Operations.subtract).get_result() == 0


# Part 1D: shared number rules and a finite result

def test_text_numbers_are_converted_to_floats():
    calculation = Calculation(("2", "3"), Operations.add)
    assert calculation.values == (2.0, 3.0)


def test_invalid_operands_are_rejected():
    with pytest.raises(ValueError, match="numeric"):
        Calculation(("hello", 1), Operations.add)
    with pytest.raises(ValueError, match="finite"):
        Calculation((float("nan"), 1), Operations.add)


def test_nonfinite_result_is_rejected():
    with pytest.raises(ValueError, match="outside the supported range"):
        Calculation((1e308, 1e308), Operations.add).get_result()


# Part 3: one collection of values and named settings

def test_one_value_calculation():
    assert Calculation((3,), Operations.square).get_result() == 9


def test_many_value_calculation():
    assert Calculation((2, 3, 4), Operations.sum).get_result() == 9


def test_values_are_unpacked_and_options_passed_by_name():
    calculation = Calculation((3,), Operations.power, exponent=4)
    assert calculation.values == (3.0,)
    assert calculation.options == {"exponent": 4}
    assert calculation.get_result() == 81


def test_options_are_copied_not_shared():
    settings = {"exponent": 3}
    calculation = Calculation((2,), Operations.power, **settings)
    settings["exponent"] = 10
    assert calculation.get_result() == 8


def test_negative_sqrt_fails_only_during_execution():
    calculation = Calculation((-1,), Operations.sqrt)
    with pytest.raises(ValueError):
        calculation.get_result()