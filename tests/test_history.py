"""Test ownership and state changes through History's public methods."""

import pytest

from calculator.calculation import Calculation
from calculator.history import History
from calculator.operations import Operations


def add(a, b):
    return Calculation((a, b), Operations.add)


def subtract(a, b):
    return Calculation((a, b), Operations.subtract)


def test_empty_history():
    assert History().get_history() == []


def test_mixed_calculations_keep_their_order():
    history = History()
    first = add(10, 5)
    second = subtract(20, 7)
    history.add(first, 15.0)
    history.add(second, 13.0)
    assert history.get_history() == [(first, 15.0), (second, 13.0)]


def test_returned_list_is_a_copy():
    history = History()
    calculation = add(10, 5)
    history.add(calculation, 15.0)
    snapshot = history.get_history()
    snapshot.clear()
    assert history.get_history() == [(calculation, 15.0)]


def test_copy_still_shares_the_calculation_objects():
    # Shallow copy limit: the list is new, the objects inside are the same.
    history = History()
    calculation = add(10, 5)
    history.add(calculation, 15.0)
    stored, saved_result = history.get_history()[0]
    assert stored is calculation
    assert saved_result == 15.0


def test_remove_returns_the_selected_entry():
    history = History()
    first = add(10, 5)
    second = subtract(20, 7)
    history.add(first, 15.0)
    history.add(second, 13.0)
    assert history.remove(0) == (first, 15.0)
    assert history.get_history() == [(second, 13.0)]
    assert history.remove(0) == (second, 13.0)
    assert history.get_history() == []


def test_invalid_removal_preserves_entries():
    history = History()
    calculation = add(10, 5)
    history.add(calculation, 15.0)
    for invalid_index in [-1, 1, 99]:
        with pytest.raises(IndexError):
            history.remove(invalid_index)
        assert history.get_history() == [(calculation, 15.0)]


def test_clear_removes_every_entry():
    history = History()
    history.add(add(1, 2), 3.0)
    history.add(add(3, 4), 7.0)
    history.clear()
    assert history.get_history() == []


def test_histories_are_independent():
    first = History()
    second = History()
    first.add(add(10, 5), 15.0)
    assert second.get_history() == []


def test_reject_non_calculation():
    history = History()
    with pytest.raises(TypeError):
        history.add("not a calculation", 1.0)
    assert history.get_history() == []


# My own tests

def test_remove_from_empty_history_raises_index_error():
    history = History()
    with pytest.raises(IndexError):
        history.remove(0)
    assert history.get_history() == []


def test_remove_middle_entry_keeps_neighbors():
    history = History()
    first = add(1, 2)
    middle = subtract(5, 1)
    last = add(10, 20)
    for calculation in [first, middle, last]:
        history.add(calculation, calculation.get_result())
    assert history.remove(1) == (middle, 4.0)
    assert history.get_history() == [(first, 3.0), (last, 30.0)]


def test_remove_last_entry_keeps_previous_order():
    history = History()
    first = add(1, 2)
    middle = subtract(5, 1)
    last = add(10, 20)
    for calculation in [first, middle, last]:
        history.add(calculation, calculation.get_result())
    assert history.remove(2) == (last, 30.0)
    assert history.get_history() == [(first, 3.0), (middle, 4.0)]