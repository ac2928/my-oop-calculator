"""Read, evaluate, print, and loop until the user exits."""

from math import isfinite

from calculator.calculation import Add, Calculation, Subtract
from calculator.history import History


HELP = """Commands:
  add       Add two numbers
  subtract  Subtract the second number from the first
  history   Show this session's calculations
  remove    Remove a calculation by its displayed number
  help      Show available commands
  exit      Exit the calculator"""


def describe(calculation: Calculation) -> str:
    """Format any calculation through its common interface."""
    return (
        f"{type(calculation).__name__}: "
        f"{calculation.a:g}, {calculation.b:g} = {calculation.get_result():g}"
    )


def show_history(history: History) -> None:
    """Display a snapshot without changing the collection."""
    calculations = history.get_history()
    if not calculations:
        print("No calculations in history.")
        return
    print("Calculation History\n")
    for number, calculation in enumerate(calculations, start=1):
        print(f"{number}. {describe(calculation)}")


def read_number(prompt: str) -> float:
    """Convert terminal text into a finite floating-point number."""
    number = float(input(prompt))
    if not isfinite(number):
        raise ValueError("A finite number is required.")
    return number


def run() -> None:
    """Run one independent calculator session."""
    history = History()
    operations = {"add": Add, "subtract": Subtract}
    print('OOP Calculator\n\nType "help" for commands.')
    while True:
        try:
            command = input("> ").strip().lower()
            if command == "exit":
                break
            if command in operations:
                try:
                    a = read_number("First number: ")
                    b = read_number("Second number: ")
                    operation_class = operations[command]
                    calculation = operation_class(a, b)
                    result = calculation.get_result()
                    if not isfinite(result):
                        raise ValueError("Result is outside the supported range.")
                except ValueError:
                    print("Invalid number or result. Please use finite numbers.")
                    continue
                history.add(calculation)
                print(f"Result: {result:g}")
            elif command == "history":
                show_history(history)
            elif command == "remove":
                show_history(history)
                if not history.get_history():
                    continue
                try:
                    number = int(input("Enter calculation number to remove: "))
                    removed = history.remove(number - 1)
                except ValueError:
                    print("Please enter a whole calculation number.")
                except IndexError:
                    print("Calculation does not exist.")
                else:
                    print(f"Removed: {describe(removed)}")
            elif command == "help":
                print(HELP)
            else:
                print('Unknown command.\nType "help" for available commands.')
        except (EOFError, KeyboardInterrupt):
            print()
            break
    print("Goodbye!")