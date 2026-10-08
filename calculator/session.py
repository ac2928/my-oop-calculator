"""Execute calculations, record successful results, and count failed executions."""

from calculator.history import History


class CalculatorSession:
    def __init__(self):
        self._history = History()
        self._failures = 0

    def calculate(self, calculation) -> float:
        try:
            result = calculation.get_result()    # if this raises, nothing is recorded
        except Exception:
            self._failures += 1                  # count the failure, then let it continue upward
            raise
        self._history.add(calculation, result)   # only reached on success
        return result

    def get_history(self):
        return self._history.get_history()

    def failure_count(self) -> int:
        return self._failures

    def clear(self) -> None:
        """Start over: clear saved successes and the failure count together."""
        self._history.clear()
        self._failures = 0