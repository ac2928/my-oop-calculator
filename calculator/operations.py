"""Stateless math operations: no prompts, files, or history."""

from math import pow, sqrt


class Operations:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        return a / b

    @staticmethod
    def square(value):
        return value * value

    @staticmethod
    def sqrt(value):
        # math.sqrt raises ValueError for a negative number.
        return sqrt(value)

    @staticmethod
    def sum(*values):
        # Python's built-in sum() returns 0 for nothing; this app requires a value.
        if not values:
            raise ValueError("Enter at least one value.")
        return sum(values)

    @staticmethod
    def power(value, *, exponent=2):
        # The bare * makes exponent keyword-only: power(3, exponent=4).
        return pow(value, exponent)