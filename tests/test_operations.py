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