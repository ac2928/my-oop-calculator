"""A CSV file only supplies values; the same validation and statistics follow."""

import pytest

from calculator.cli import run
from calculator.factory import CalculationFactory
from calculator.inputs import read_csv_values


def write_csv(tmp_path, text, name="data.csv"):
    path = tmp_path / name
    path.write_text(text)
    return path


def session(monkeypatch, capsys, answers):
    responses = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt: next(responses))
    run()
    return capsys.readouterr().out


# Reading the file

def test_reads_the_value_column(tmp_path):
    path = write_csv(tmp_path, "label,value\na,10\nb,20\n")
    assert read_csv_values(path) == [10, 20]


def test_supplied_values_csv():
    assert read_csv_values("values.csv") == [10, 20, 30, 40, 50]


def test_missing_value_column(tmp_path):
    path = write_csv(tmp_path, "amount\n1\n2\n")
    with pytest.raises(ValueError, match="column named value"):
        read_csv_values(path)


def test_completely_blank_lines_are_skipped(tmp_path):
    path = write_csv(tmp_path, "value\n10\n\n30\n")
    assert read_csv_values(path) == [10, 30]


def test_quoted_empty_cell_fails_numeric_validation(tmp_path):
    # pandas reads it as a missing value; our shared rules refuse it.
    path = write_csv(tmp_path, 'value\n10\n""\n30\n')
    values = read_csv_values(path)
    with pytest.raises(ValueError, match="finite"):
        CalculationFactory.create("mean", *values)


def test_missing_file_raises():
    with pytest.raises(OSError):
        read_csv_values("does-not-exist.csv")


# Same answer from either source

def test_csv_and_typed_values_match(tmp_path):
    path = write_csv(tmp_path, "value\n2\n4\n6\n")
    from_file = CalculationFactory.create("stddev", *read_csv_values(path)).get_result()
    typed = CalculationFactory.create("stddev", 2, 4, 6).get_result()
    assert from_file == typed


# Through the CLI

def test_cli_csv_requests(monkeypatch, capsys):
    output = session(monkeypatch, capsys, [
        "stddev 10 20 30 40 50", "csv stddev values.csv", "csv mean values.csv",
        "stddev 2 4 6 ddof=0", "csv stddev values.csv ddof=0", "exit",
    ])
    assert output.count("Result: 15.8114") == 2
    assert "Result: 30.0000" in output
    assert "Result: 1.6330" in output
    assert "Result: 14.1421" in output


def test_cli_csv_failures_then_success(monkeypatch, capsys, tmp_path):
    no_column = write_csv(tmp_path, "amount\n1\n", "no_column.csv")
    empty = write_csv(tmp_path, "", "empty.csv")
    broken = write_csv(tmp_path, 'value\n"1\n', "broken.csv")
    text = write_csv(tmp_path, "value\n1\nabc\n", "text.csv")
    one = write_csv(tmp_path, "value\n7\n", "one.csv")
    output = session(monkeypatch, capsys, [
        "csv mean", "csv sum values.csv", f"csv mean {no_column}",
        f"csv mean {empty}", f"csv mean {broken}", f"csv mean {text}",
        f"csv stddev {one}", "csv mean nowhere.csv",
        "mean 2 4", "history", "exit",
    ])
    assert "Error: Use: csv mean/stddev PATH" in output
    assert "Error: CSV supports mean or stddev." in output
    assert "Error: CSV must contain a column named value." in output
    assert "Error: Values must be numeric." in output
    assert "Error: Enter at least two values." in output
    assert "No such file" in output
    assert output.count("Error:") == 8
    # A failed file request is followed by a successful typed one.
    assert "Result: 3.0000" in output
    assert output.endswith("mean 2 4 = 3.0000\nGoodbye!\n")