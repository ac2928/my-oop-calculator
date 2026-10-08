"""My adaptation: a summary action counting successes and failed executions."""

import pytest

from calculator.cli import run
from calculator.commands import ClearHistoryCommand, SummaryCommand
from calculator.factory import CalculationFactory
from calculator.sequence import execute_sequence
from calculator.session import CalculatorSession


def test_new_session_summary():
    assert SummaryCommand(CalculatorSession()).execute() == "Successful: 0, Failed: 0"


def test_failure_is_counted_but_never_saved_in_history():
    session = CalculatorSession()
    session.calculate(CalculationFactory.create("add", 2, 3))
    with pytest.raises(ZeroDivisionError):
        session.calculate(CalculationFactory.create("divide", 1, 0))
    assert session.failure_count() == 1
    assert len(session.get_history()) == 1
    assert SummaryCommand(session).execute() == "Successful: 1, Failed: 1"


def test_clear_resets_both_counts():
    session = CalculatorSession()
    execute_sequence(session, [
        CalculationFactory.create("add", 1, 1),
        CalculationFactory.create("sqrt", -9),
    ])
    assert SummaryCommand(session).execute() == "Successful: 1, Failed: 1"
    ClearHistoryCommand(session).execute()
    assert SummaryCommand(session).execute() == "Successful: 0, Failed: 0"


def test_cli_summary_counts_execution_failures_only(monkeypatch, capsys):
    answers = iter([
        "add 2 3", "divide 1 0", "sqrt -1",   # 1 success, 2 failures while running the math
        "add abc 1", "pizza 1 2",             # rejected before a calculation exists: not counted
        "summary", "clear", "summary", "summary now", "exit",
    ])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    run()
    output = capsys.readouterr().out
    assert "Successful: 1, Failed: 2" in output
    assert "Successful: 0, Failed: 0" in output
    assert "Error: summary does not accept values." in output