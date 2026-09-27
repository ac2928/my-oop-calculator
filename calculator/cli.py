"""A happy-path REPL. Stage 5 will handle invalid numeric input."""

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
    """Format an object through its common interface."""
    return (
        f"{type(calculation).__name__}: "
        f"{calculation.a:g}, {calculation.b:g} = {calculation.get_result():g}"
    )


def show_history(history: History) -> None:
    calculations = history.get_history()
    if not calculations:
        print("No calculations in history.")
        return
    print("Calculation History\n")
    for number, calculation in enumerate(calculations, start=1):
        print(f"{number}. {describe(calculation)}")


def run() -> None:
    history = History()
    operations = {"add": Add, "subtract": Subtract}
    print('OOP Calculator\n\nType "help" for commands.')
    while True:
        command = input("> ").strip().lower()
        if command == "exit":
            break
        if command in operations:
            a = float(input("First number: "))
            b = float(input("Second number: "))
            operation_class = operations[command]
            calculation = operation_class(a, b)
            history.add(calculation)
            print(f"Result: {calculation.get_result():g}")
        elif command == "history":
            show_history(history)
        elif command == "remove":
            show_history(history)
            if history.get_history():
                number = int(input("Enter calculation number to remove: "))
                removed = history.remove(number - 1)
                print(f"Removed: {describe(removed)}")
        elif command == "help":
            print(HELP)
        else:
            print('Unknown command.\nType "help" for available commands.')
    print("Goodbye!")