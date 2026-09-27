"""Manage a collection of calculation objects."""

from calculator.calculation import Calculation


class History:
    """Own session history and expose controlled access to its collection."""

    def __init__(self) -> None:
        self._calculations: list[Calculation] = []

    def add(self, calculation: Calculation) -> None:
        """Append a calculation to history."""
        if not isinstance(calculation, Calculation):
            raise TypeError("History accepts Calculation objects only.")
        self._calculations.append(calculation)

    def get_history(self) -> list[Calculation]:
        """Return a copy so callers cannot modify the internal list."""
        return self._calculations.copy()

    def remove(self, index: int) -> Calculation:
        """Remove and return a calculation by its zero-based index."""
        if index < 0 or index >= len(self._calculations):
            raise IndexError("Calculation does not exist.")
        return self._calculations.pop(index)