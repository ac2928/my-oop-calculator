"""Commands represent application actions; each one shares execute() -> str."""

from abc import ABC, abstractmethod


HELP = (
    "Commands: add/subtract/multiply/divide A B; square/sqrt VALUE; "
    "power VALUE exponent=N; sum/mean/stddev VALUES (stddev ddof=0/1); "
    "csv mean/stddev PATH; history; clear; help; exit"
)


class Command(ABC):
    @abstractmethod
    def execute(self) -> str:
        """Perform an action and return display text; expected errors may propagate."""


class CalculateCommand(Command):
    def __init__(self, session, calculation):
        self.session = session
        self.calculation = calculation

    def execute(self) -> str:
        result = self.session.calculate(self.calculation)
        return f"Result: {result:.4f}"


class HistoryCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        lines = []
        for calculation, result in self.session.get_history():
            values = " ".join(f"{value:g}" for value in calculation.values)
            options = " ".join(f"{key}={value:g}" for key, value in calculation.options.items())
            request = " ".join(part for part in (calculation.operation.__name__, values, options) if part)
            lines.append(f"{request} = {result:.4f}")   # saved result: no math is rerun
        return "\n".join(lines) or "History is empty."


class ClearHistoryCommand(Command):
    def __init__(self, session):
        self.session = session

    def execute(self) -> str:
        self.session.clear()
        return "History cleared."


class HelpCommand(Command):
    def execute(self) -> str:
        return HELP