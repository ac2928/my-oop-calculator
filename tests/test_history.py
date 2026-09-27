"""Test ownership and state changes through History's public methods."""

import pytest

from calculator.calculation import Add, Subtract
from calculator.history import History


def test_empty_history():
    assert History().get_history() == []


def test_mixed_calculations_keep_their_order():
    history = History()
    first = Add(10, 5)
    second = Subtract(20, 7)
    history.add(first)
    history.add(second)
    assert history.get_history() == [first, second]


def test_returned_list_is_a_copy():
    history = History()
    calculation = Add(10, 5)
    history.add(calculation)
    snapshot = history.get_history()
    snapshot.clear()
    assert history.get_history() == [calculation]


def test_remove_returns_the_selected_object():
    history = History()
    first = Add(10, 5)
    second = Subtract(20, 7)
    history.add(first)
    history.add(second)
    # is checks identity: we receive the same object that was stored.
    assert history.remove(0) is first
    assert history.get_history() == [second]
    assert history.remove(0) is second
    assert history.get_history() == []


def test_invalid_removal_preserves_entries():
    history = History()
    calculation = Add(10, 5)
    history.add(calculation)
    for invalid_index in [-1, 1, 99]:
        with pytest.raises(IndexError):
            history.remove(invalid_index)
        assert history.get_history() == [calculation]


def test_histories_are_independent():
    first = History()
    second = History()
    first.add(Add(10, 5))
    assert second.get_history() == []


def test_reject_non_calculation():
    history = History()
    with pytest.raises(TypeError):
        history.add("not a calculation")
    assert history.get_history() == []





# My own test

def test_remove_from_empty_history_raises_index_error():
    history = History()
    with pytest.raises(IndexError):
        history.remove(0)
    assert history.get_history() == []