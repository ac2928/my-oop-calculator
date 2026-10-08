"""Different actions share one contract: execute() returns display text."""

import pytest

from calculator.commands import (
    HELP, CalculateCommand, ClearHistoryCommand, Command, HelpCommand, HistoryCommand,
)
from calculator.factory import CalculationFactory
from calculator.session import CalculatorSession


def test_calculate_command_returns_text_and_records():
    session = CalculatorSession()
    command = CalculateCommand(session, CalculationFactory.create("add", 2, 3))
    assert session.get_history() == []      # building the command did no math
    assert command.execute() == "Result: 5.0000"
    assert len(session.get_history()) == 1


def test_failed_calculate_command_records_nothing():
    session = CalculatorSession()
    command = CalculateCommand(session, CalculationFactory.create("divide", 1, 0))
    with pytest.raises(ZeroDivisionError):
        command.execute()
    assert HistoryCommand(session).execute() == "History is empty."


def test_history_command_shows_saved_requests():
    session = CalculatorSession()
    CalculateCommand(session, CalculationFactory.create("add", 2, 3)).execute()
    CalculateCommand(session, CalculationFactory.create("power", 3, exponent=4)).execute()
    assert HistoryCommand(session).execute() == (
        "add 2 3 = 5.0000\npower 3 exponent=4 = 81.0000"
    )


def test_clear_command_uses_the_session():
    session = CalculatorSession()
    CalculateCommand(session, CalculationFactory.create("add", 2, 3)).execute()
    assert ClearHistoryCommand(session).execute() == "History cleared."
    assert HistoryCommand(session).execute() == "History is empty."


def test_help_command():
    assert HelpCommand().execute() == HELP


def test_one_loop_runs_different_commands():
    # Polymorphism: the caller only needs execute().
    session = CalculatorSession()
    commands = [
        CalculateCommand(session, CalculationFactory.create("add", 2, 3)),
        HistoryCommand(session),
        ClearHistoryCommand(session),
        HelpCommand(),
    ]
    outputs = [command.execute() for command in commands]
    assert outputs == ["Result: 5.0000", "add 2 3 = 5.0000", "History cleared.", HELP]


def test_command_is_abstract():
    with pytest.raises(TypeError):
        Command()


def test_subclass_without_execute_cannot_be_created():
    # The lesson's check: an incomplete subclass is refused.
    class Incomplete(Command):
        pass

    with pytest.raises(TypeError):
        Incomplete()