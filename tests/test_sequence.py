"""A failure in a sequence must not stop later calculations."""

from calculator.factory import CalculationFactory
from calculator.sequence import execute_sequence
from calculator.session import CalculatorSession


def test_worked_request_later_success_after_failure():
    # Lesson's worked request: add 2 3, divide 1 0, square 3.
    session = CalculatorSession()
    calculations = [
        CalculationFactory.create("add", 2, 3),
        CalculationFactory.create("divide", 1, 0),
        CalculationFactory.create("square", 3),
    ]
    results, errors = execute_sequence(session, calculations)
    assert results == [5.0, 9.0]                   # the item AFTER the failure still ran
    assert errors == ["float division by zero"]
    assert [result for _, result in session.get_history()] == [5.0, 9.0]


def test_every_item_failing_leaves_history_empty():
    session = CalculatorSession()
    calculations = [
        CalculationFactory.create("sqrt", -1),
        CalculationFactory.create("add", 1e308, 1e308),
    ]
    results, errors = execute_sequence(session, calculations)
    assert results == []
    assert len(errors) == 2
    assert session.get_history() == []


def test_empty_sequence():
    assert execute_sequence(CalculatorSession(), []) == ([], [])