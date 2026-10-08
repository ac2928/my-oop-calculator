# OOP Calculator

A command-line calculator built with object-oriented Python, extended with a calculation factory, command objects, pandas statistics, and CSV input. Type one request per line, for example: add 2 3, power 3 exponent=4, mean 2 4 6, stddev 10 20 30 40 50, csv mean values.csv, history, summary, clear, help, exit. See LEARNING_LOG.md for design explanations for each part.

## Installation

Requires Python 3.11 or newer.

    git clone https://github.com/ac2928/my-oop-calculator.git
    cd my-oop-calculator
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Running

    python -m calculator

Type help to see the available commands.

## Testing

    python -m pytest

This runs every test and fails if line or branch coverage drops below 100%.

## Design choices

These notes describe the original calculator. See LEARNING_LOG.md for how the design changed in each part of this extension.

- Calculation is an abstract parent that holds two values. Add and Subtract reuse this, but override get_result() to provide their own implementation. The duplicated `__init__` code has been eliminated.

- The CLI uses a dictionary to hold the operation types. When requested the appropriate class is instantiated and get_result() is called. There is no determination of Add or Subtract. This is polymorphism.

- History uses an internal list (_calculations) which can only be manipulated by the add and remove methods. get_history() returns a copy so external code can’t accidentally change or reorder the internal list.

- Prior to passing control to history.add(), both the two values and the result are verified as finite. Failed operations are not stored. Invalid data results in a message and return to the loop rather than crashing.

## Reflection

**Where would Multiply belong?**
I would create a Multiply class in calculation.py that is a subclass of Calculation and has the method return self.a * self.b. I would also add "multiply": Multiply to the operations dictionary, add it to the help text and add tests for the class and the CLI. History would not need to be modified since it uses any Calculation and agrees on the same get_result() method.

**What could email and text-message notifications share?**
I would create a Notification class that has a message and recipient and an abstract send() method. EmailNotification and TextNotification would each have a different implementation of send(). The client code could then create a list of notifications and iterate through them calling send() on each without needing to know the type of the notification.

**What transfers to another language?**
The concepts would move over including encapsulation, inheritance, polymorphism, abstraction, testing via CI and assertions, classes and instances. What would need to be learned for the other language would be error handling, data types, syntax, interface/abstract class support and testing support.

## Notes

**One confusing instruction and how I'd improve it:**
The exercise instructed to type entrypoint.py into `calculator/__main__.py`. I originally misnamed the file and received the error, No module named `calculator.__main__`. I would document the requirement for two underscores on either side of the name and also reference this error to aid the student in understanding its significance.

**If tests pass but coverage fails:**
I would read the Missing column of the coverage report to determine which lines or branches were not executed. I would then determine user actions that would cause these lines or branches to be executed and write a test that verifies this behavior. I would not remove lines of code or delete functionality in order to increase the coverage percentage.