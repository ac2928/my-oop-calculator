"""Manage the session's history of calculations and their results."""

from calculator.calculation import Calculation


class History:
    """Own session history and expose controlled access to its entries."""

    def __init__(self) -> None:
        self._entries = []

    def add(self, calculation, result) -> None:
        """Save a calculation together with the result it already produced."""
        if not isinstance(calculation, Calculation):
            raise TypeError("History accepts Calculation objects only.")
        self._entries.append((calculation, result))

    def get_history(self):
        """Return a copy: the list is new, but the Calculation objects are shared."""
        return self._entries.copy()

    def remove(self, index: int):
        """Remove and return one (calculation, result) entry by zero-based index."""
        if index < 0 or index >= len(self._entries):
            raise IndexError("Calculation does not exist.")
        return self._entries.pop(index)

    def clear(self) -> None:
        self._entries.clear()