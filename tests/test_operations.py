"""Static operations are called on the class, without creating an object."""

import pytest

from calculator.operations import Operations


def test_add():
    assert Operations.add(2, 3) == 5


def test_subtract():
    assert Operations.subtract(10, 4) == 6


def test_multiply():
    assert Operations.multiply(3, 4) == 12


def test_divide():
    assert Operations.divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Operations.divide(1, 0)


# Part 3B: one value and many values

def test_square():
    assert Operations.square(-3) == 9


def test_sqrt():
    assert Operations.sqrt(9) == 3


def test_negative_sqrt_raises():
    with pytest.raises(ValueError):
        Operations.sqrt(-1)


def test_sum_accepts_one_or_many_values():
    assert Operations.sum(7) == 7
    assert Operations.sum(2, 3, 4) == 9


def test_sum_needs_at_least_one_value():
    with pytest.raises(ValueError, match="at least one"):
        Operations.sum()


# Part 3C: a named setting

def test_power_default_exponent_is_two():
    assert Operations.power(5) == 25


def test_power_with_named_exponent():
    assert Operations.power(3, exponent=4) == 81


def test_power_exponent_must_be_named():
    # power(3, 4) is rejected: exponent can only be given by name.
    with pytest.raises(TypeError):
        Operations.power(3, 4)