"""The session computes first and records only successful results."""

import pytest

from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def test_successful_calculation_is_recorded():
    session = CalculatorSession()
    calculation = CalculationFactory.create("add", 2, 3)
    assert session.calculate(calculation) == 5.0
    assert session.get_history() == [(calculation, 5.0)]


def test_failed_calculation_leaves_history_unchanged():
    session = CalculatorSession()
    first = CalculationFactory.create("add", 2, 3)
    session.calculate(first)
    with pytest.raises(ZeroDivisionError):
        session.calculate(CalculationFactory.create("divide", 1, 0))
    assert session.get_history() == [(first, 5.0)]


def test_clear_empties_history():
    session = CalculatorSession()
    session.calculate(CalculationFactory.create("add", 1, 1))
    session.clear()
    assert session.get_history() == []


def test_sessions_are_independent():
    first = CalculatorSession()
    second = CalculatorSession()
    first.calculate(CalculationFactory.create("add", 1, 1))
    assert second.get_history() == []


def test_changing_the_returned_list_does_not_change_history():
    session = CalculatorSession()
    calculation = CalculationFactory.create("add", 2, 3)
    session.calculate(calculation)
    snapshot = session.get_history()
    snapshot.clear()
    snapshot.append(("fake", 0))
    assert session.get_history() == [(calculation, 5.0)]