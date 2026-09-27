"""A test conversation provides input and checks what the app prints."""

from calculator.cli import run


def session(monkeypatch, capsys, answers):
    responses = iter(answers)

    def scripted_input(prompt):
        return next(responses)

    monkeypatch.setattr("builtins.input", scripted_input)
    run()
    return capsys.readouterr().out


def test_arithmetic_session(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add", "10", "5", "subtract", "20", "7", "exit"])
    assert "Result: 15" in output
    assert "Result: 13" in output
    assert output.endswith("Goodbye!\n")


def test_history_and_removal(monkeypatch, capsys):
    output = session(monkeypatch, capsys,
                     ["add", "10", "5", "subtract", "20", "7",
                      "history", "remove", "1", "history", "exit"])
    assert "1. Add: 10, 5 = 15" in output
    assert "2. Subtract: 20, 7 = 13" in output
    assert "Removed: Add: 10, 5 = 15" in output
    assert output.endswith("1. Subtract: 20, 7 = 13\nGoodbye!\n")


def test_empty_history(monkeypatch, capsys):
    output = session(monkeypatch, capsys, ["history", "remove", "exit"])
    assert output.count("No calculations in history.") == 2


def test_help_and_unknown_command(monkeypatch, capsys):
    output = session(monkeypatch, capsys, [" HELP ", "pizza", " EXIT "])
    assert "Commands:" in output
    assert "Unknown command." in output
    assert output.endswith("Goodbye!\n")





    # My own test:
def test_mixed_case_arithmetic_session(monkeypatch, capsys):
    output = session(monkeypatch, capsys, [" aDd ", " 8 ", " 12 ", "exit"])
    assert "Result: 20" in output
    assert output.endswith("Goodbye!\n")