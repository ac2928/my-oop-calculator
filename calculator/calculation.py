"""A shared calculation contract and its concrete implementations."""

from abc import ABC, abstractmethod


class Calculation(ABC):
    """Store two operands and require subclasses to provide a result."""

    def __init__(self, a: float, b: float) -> None:
        self.a = a
        self.b = b

    @abstractmethod
    def get_result(self) -> float:
        """Return the result of this calculation."""


class Add(Calculation):
    """Add the two operands."""

    def get_result(self) -> float:
        return self.a + self.b


class Subtract(Calculation):
    """Subtract the second operand from the first."""

    def get_result(self) -> float:
        return self.a - self.b