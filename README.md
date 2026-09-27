# OOP Calculator

A command-line calculator built with object-oriented Python. It supports add, subtract, history, remove, help, and exit.

## Installation

Requires Python 3.11 or newer.

    git clone https://github.com/ac2928/my-oop-calculator.git
    cd my-oop-calculator
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Running

    python -m calculator

Type `help` to see the available commands.

## Testing

    python -m pytest

This runs every test and fails if line or branch coverage drops below 100%.

## Design choices

- `Calculation` is an abstract parent class that stores the two operands once. `Add` and `Subtract` inherit that setup and each supply their own `get_result()`, which removed the duplicated `__init__` code.
- The CLI keeps the operation classes in a dictionary, creates whichever one the user asked for, and calls `get_result()` on it. It never checks whether it has an `Add` or a `Subtract`; that's polymorphism.
- `History` keeps its list internal (`_calculations`) and only changes it through `add` and `remove`. `get_history()` returns a copy, so outside code can't accidentally erase or reorder the real list.
- The CLI checks that both numbers and the result are finite before calling `history.add()`, so failed calculations never get saved. Bad input prints a message and the loop continues instead of crashing.

## Reflection

**Where would Multiply belong?**
I'd add a `Multiply` class to `calculation.py` that inherits from `Calculation` and returns `self.a * self.b`. Then I'd add `"multiply": Multiply` to the operations dictionary, a line to the help text, and tests for the class and a CLI session. `History` needs no changes, because it stores any `Calculation` and only relies on the shared `get_result()` contract.

**What could email and text-message notifications share?**
An abstract `Notification` parent could store the recipient and message and declare an abstract `send()` method. `EmailNotification` and `TextNotification` would each implement `send()` their own way, so the calling code could loop through notifications and call `send()` without checking their type.

**What transfers to another language?**
The design ideas carry over: classes and instances, abstraction, inheritance, polymorphism, encapsulation, and testing with assertions and CI. What I'd still need to learn is that language's syntax, how it declares abstract classes or interfaces, how it handles errors and types, and its testing tools.

## Notes

**One confusing instruction and how I'd improve it:**
The lesson said to type `entrypoint.py` into `calculator/__main__.py`. I named the file wrong at first and got "No module named calculator.__main__". I'd improve it by spelling out that the name needs two underscores on each side, and by mentioning that error so students know what it means.

**If tests pass but coverage fails:**
I'd read the Missing column in the coverage table to find which lines or branches never ran, figure out what user behavior would reach them, and add a test that asserts the expected outcome. I wouldn't delete code or exclude lines just to raise the percentage.