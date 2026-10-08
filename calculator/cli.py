"""Read, evaluate, print, and loop until the user exits."""

from math import isfinite

from calculator.calculation import Calculation
from calculator.factory import CalculationFactory
from calculator.history import History


HELP = """Commands:
  add       Add two numbers
  subtract  Subtract the second number from the first
  multiply  Multiply two numbers
  divide    Divide the first number by the second
  history   Show this session's calculations
  remove    Remove a calculation by its displayed number
  help      Show available commands
  exit      Exit the calculator"""


def describe(calculation: Calculation, result: float) -> str:
    """Format a calculation and its saved result (no math is rerun)."""
    return (
        f"{calculation.operation.__name__.capitalize()}: "
        f"{', '.join(f'{value:g}' for value in calculation.values)} = {result:g}"
    )


def show_history(history: History) -> None:
    """Display a snapshot without changing the collection."""
    entries = history.get_history()
    if not entries:
        print("No calculations in history.")
        return
    print("Calculation History\n")
    for number, (calculation, result) in enumerate(entries, start=1):
        print(f"{number}. {describe(calculation, result)}")


def read_number(prompt: str) -> float:
    """Convert terminal text into a finite floating-point number."""
    number = float(input(prompt))
    if not isfinite(number):
        raise ValueError("A finite number is required.")
    return number


# This prompt-per-number CLI asks for exactly two numbers, so it offers only
# the two-value operations. Part 4 replaces it with one-line requests.
TWO_VALUE_COMMANDS = {"add", "subtract", "multiply", "divide"}


def run() -> None:
    """Run one independent calculator session."""
    history = History()
    print('OOP Calculator\n\nType "help" for commands.')
    while True:
        try:
            command = input("> ").strip().lower()
            if command == "exit":
                break
            if command in TWO_VALUE_COMMANDS:
                try:
                    a = read_number("First number: ")
                    b = read_number("Second number: ")
                    calculation = CalculationFactory.create(command, a, b)
                    result = calculation.get_result()
                except ValueError:
                    print("Invalid number or result. Please use finite numbers.")
                    continue
                except ZeroDivisionError:
                    print("Cannot divide by zero.")
                    continue
                history.add(calculation, result)
                print(f"Result: {result:g}")
            elif command == "history":
                show_history(history)
            elif command == "remove":
                show_history(history)
                if not history.get_history():
                    continue
                try:
                    number = int(input("Enter calculation number to remove: "))
                    calculation, result = history.remove(number - 1)
                except ValueError:
                    print("Please enter a whole calculation number.")
                except IndexError:
                    print("Calculation does not exist.")
                else:
                    print(f"Removed: {describe(calculation, result)}")
            elif command == "help":
                print(HELP)
            else:
                print('Unknown command.\nType "help" for available commands.')
        except (EOFError, KeyboardInterrupt):
            print()
            break
    print("Goodbye!")