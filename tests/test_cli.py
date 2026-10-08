"""A scripted terminal conversation checks what the app prints.

Part 4 changed the protocol from one prompt per number ("add", "10", "5") to
one request per line ("add 10 5"). These tests keep the earlier behaviors
(results, history, recovery, clean exit) under the new protocol. The old
"remove" action was replaced by "clear".
"""

import runpy

from calculator.cli import prepare_command, run
from calculator.commands import CalculateCommand, HelpCommand, HistoryCommand
from calculator.session import CalculatorSession


def session(monkeypatch, capsys, answers):
    responses = iter(answers)

    def scripted_input(prompt):
        return next(responses)

    monkeypatch.setattr("builtins.input", scripted_input)
    run()
    return capsys.readouterr().out


# prepare_command builds commands; it never runs them

def test_prepare_command_builds_without_running():
    calculator_session = CalculatorSession()
    command = prepare_command("add 2 3", calculator_session)
    assert isinstance(command, CalculateCommand)
    assert calculator_session.get_history() == []   # nothing ran yet
    assert command.execute() == "Result: 5.0000"


def test_prepare_command_reads_values_and_settings():
    command = prepare_command("power 3 exponent=4", CalculatorSession())
    assert command.calculation.values == (3.0,)
    assert command.calculation.options == {"exponent": 4.0}


def test_prepare_command_for_actions():
    calculator_session = CalculatorSession()
    assert isinstance(prepare_command("history", calculator_session), HistoryCommand)
    assert isinstance(prepare_command("HELP", calculator_session), HelpCommand)


# Full sessions

def test_arithmetic_session(monkeypatch, capsys):
    output = session(monkeypatch, capsys, ["add 10 5", "subtract 20 7", "exit"])
    assert "Result: 15.0000" in output
    assert "Result: 13.0000" in output
    assert output.endswith("Goodbye!\n")


def test_all_operations(monkeypatch, capsys):
    output = session(monkeypatch, capsys, [
        "multiply 2 3", "divide 7 2", "square 3", "sqrt 9",
        "power 3 exponent=4", "power 5", "sum 2 3 4", "exit",
    ])
    for expected in ["6.0000", "3.5000", "9.0000", "3.0000", "81.0000", "25.0000"]:
        assert f"Result: {expected}" in output


def test_history_then_clear(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add 10 5", "power 3 exponent=4", "history", "clear", "history", "exit"])
    assert "add 10 5 = 15.0000\npower 3 exponent=4 = 81.0000" in output
    assert "History cleared." in output
    assert output.endswith("History is empty.\nGoodbye!\n")


def test_help_and_unknown_command(monkeypatch, capsys):
    output = session(monkeypatch, capsys, ["help", "pizza 1 2", " EXIT "])
    assert "Commands:" in output
    assert "Error: Unknown operation: pizza" in output
    assert output.endswith("Goodbye!\n")


def test_mixed_case_request(monkeypatch, capsys):
    output = session(monkeypatch, capsys, ["  aDd 8 12 ", "exit"])
    assert "Result: 20.0000" in output


def test_divide_by_zero_recovers_without_history(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["divide 1 0", "history", "add 2 3", "history", "exit"])
    assert "Error:" in output and "division by zero" in output
    assert "History is empty." in output
    assert "add 2 3 = 5.0000" in output


def test_invalid_numbers_recover_without_history(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add hello 3", "add nan 1", "history", "exit"])
    assert "Error: Values must be numeric." in output
    assert "Error: Values must be finite numbers." in output
    assert "History is empty." in output


def test_overflow_and_negative_sqrt_recover(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add 1e308 1e308", "sqrt -4", "history", "exit"])
    assert "Error: Result is outside the supported range." in output
    assert output.count("Error:") == 2
    assert "History is empty." in output


def test_bad_counts_and_settings(monkeypatch, capsys):
    output = session(monkeypatch, capsys, [
        "add 1", "power 2 exponent=3 exponent=4", "power 2 =3",
        "add 1 2 exponent=2", "history 1", "help me", "exit",
    ])
    assert "Error: add requires exactly 2 value(s)." in output
    assert output.count("Error: Options need unique names: key=value.") == 2
    assert "Error: Unsupported option for add: exponent" in output
    assert "Error: history does not accept values." in output
    assert "Error: help does not accept values." in output


def test_blank_line_reports_error(monkeypatch, capsys):
    output = session(monkeypatch, capsys, ["", "exit"])
    assert "Error: Enter a command" in output


def test_interrupted_input_exits_cleanly(monkeypatch, capsys):
    for interruption in [EOFError, KeyboardInterrupt]:
        responses = iter(["add 1 2"])

        def interrupted_input(prompt):
            try:
                return next(responses)
            except StopIteration:
                raise interruption from None

        monkeypatch.setattr("builtins.input", interrupted_input)
        run()
        assert capsys.readouterr().out.endswith("\nGoodbye!\n")


def test_module_entrypoint(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt: "exit")
    runpy.run_module("calculator", run_name="__main__")
    output = capsys.readouterr().out
    assert output.startswith("Calculator")
    assert output.endswith("Goodbye!\n")