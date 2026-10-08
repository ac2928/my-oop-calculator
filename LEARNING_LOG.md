# Learning log

## Part 1: Refactor the calculator

**What changed:** Math moved into Operations (static methods). Add and Subtract were replaced by one Calculation(a, b, operation) that stores the function and only runs it in get_result(). Number checks moved to validation.py. History now saves (calculation, result) pairs.

**Self-check**
- *What does self refer to?* The specific Calculation object, like the one holding 2, 3, and add.
- *Why is Operations static?* Its methods don't need any stored data. The two numbers passed in are everything they need, so no object or self is required.
- *What has happened right after construction?* The numbers are checked and stored, and the function is stored.
- *What has not happened?* The math. It only runs when get_result() is called. My spy test proves this.
- *Why store a result with its calculation?* So history can be shown without redoing the math.

**Callable vs. call:** Operations.add is the function itself (stored). Operations.add(2, 3) runs it and gives 5.

**Corrected prediction:** I predicted Calculation(1, 0, Operations.divide) would fail right away. It didn't: it was created fine and only failed when get_result() ran, because creating it doesn't do the math.



## Part 2: Create calculations from a name

**What changed:** A new CalculationFactory in factory.py holds the name-to-operation dictionary and has one method, create(name, a, b). The CLI no longer keeps its own dictionary; it asks CalculationFactory.create(...) for a calculation. So the rules for turning a name like "add" into a calculation now live in one place.

**Trace:** create(" ADD ", "2", "3") cleans the name to "add", looks up Operations.add, and returns a Calculation holding 2.0, 3.0 and that function. No math has run yet. Calling get_result() runs it and returns 5.0.

**Where errors happen:**
- An unknown name like pizza fails inside create, during the lookup, so no calculation is ever built.
- Dividing by zero does not fail in create. create("divide", 1, 0) builds fine, and the error only appears when get_result() runs. My test test_zero_division_fails_only_in_get_result proves this.

**Creation vs. execution (in my own words):** Building a calculation just writes down the request: the numbers and which math to use. Running it is a separate, later step where the math actually happens. Keeping these apart means a request can be built, saved or checked without doing the math, and a math error only shows up when someone asks for the answer.

**Why the lookup uses try/except:** Python raises KeyError for a name that isn't in the dictionary. Only the lookup sits inside the try, so that error becomes a clear ValueError("Unknown operation: ..."), and any other error isn't mislabeled as an unknown name.



## Part 3: One, two, and many operands

**What changed:** Calculation now stores a tuple of values plus a dictionary of named settings, Calculation(values, operation, **options), instead of a and b. get_result() calls operation(*values, **options). I added square, sqrt, sum, and power (with a named exponent setting, default 2). The factory became create(name, *values, **options).

**Why the old a/b interface changed:** square and sqrt need only one number, and sum needs any amount. With a fixed a and b, a one-number operation would need a fake second number, and sum could not be represented at all. A collection of values fits one, two, or many.

**Why the factory still needs checks:** Flexible syntax does not mean any input is accepted. The factory checks that add, subtract, multiply, and divide get exactly 2 values, square, sqrt, and power get exactly 1, and only power accepts the exponent setting. These checks happen before a calculation is built. sum checks for at least one value itself, because Python's own sum() would quietly return 0 for nothing, and this app's rule is different.

**Gather vs. unpack:**
- In a definition, *values gathers numbers into a tuple, and **options gathers named settings into a dictionary (for example, create(name, *values, **options)).
- In a call, *values unpacks a list into separate numbers, and **options unpacks a dictionary into named settings (for example, operation(*self.values, **self.options)).

**Trace:** create("power", *[3], **{"exponent": 4}) gathers values (3,) and options {"exponent": 4}, checks the count and setting, and builds a Calculation. No math runs yet. get_result() unpacks them into power(3.0, exponent=4.0) and returns 81.0.

**Errors during execution, not creation:** sqrt(-4) builds fine and only fails when get_result() runs, the same as dividing by zero.

**Note on the CLI:** The CLI still asks for two numbers one at a time, so for now it only offers add, subtract, multiply, and divide. The one-line CLI comes in Part 4.



## Part 4: Turn application actions into commands

**What changed:** A new CalculatorSession (session.py) does the math and saves only successful results. A new commands.py has an abstract Command with execute() -> str, and four actions: CalculateCommand, HistoryCommand, ClearHistoryCommand, HelpCommand. The CLI now reads one line per request (like add 2 3 or power 3 exponent=4), uses the supplied prepare_command to build a command, prints what execute() returns, and repeats. The old remove action was replaced by clear.

**Roles:** The session is the receiver (it does the work). The CLI is the invoker (it calls execute()). The factory still only builds calculations; it is not a command.

**Trace: add 2 3 (success)**
CLI reads "add 2 3" -> prepare_command splits it into add, 2, 3 -> factory looks up add and builds a Calculation holding (2.0, 3.0) -> wrapped in a CalculateCommand (no math yet) -> CLI calls execute() -> session.calculate() -> get_result() -> Operations.add(2.0, 3.0) = 5.0 -> session saves (calculation, 5.0) in history -> execute() returns "Result: 5.0000" -> CLI prints it.

**Trace: divide 1 0 (failure)**
The factory builds the



## Part 5: Statistics and another input source

**What changed:** statistics.py adds mean and standard_deviation using pandas. Operations.mean and Operations.stddev hand off to them, and the factory registers both (stddev accepts ddof as a setting). inputs.py reads the value column from a CSV. The CLI's csv mean/stddev PATH request reads the file, then builds an ordinary CalculateCommand through the same factory.

**Policy (from 2, 4, 6):** mean is 4. Squared deviations total 8. Sample deviation (ddof=1, the default) divides by n-1 = 2, so 4, and its square root is 2. Population deviation (ddof=0) divides by n = 3, about 1.6330. This app's rules: mean needs at least 1 value; stddev needs at least 2 for both settings; ddof must be 0 or 1.

**Predictions:** Three identical values (7, 7, 7): mean is 7 and deviation is 0. A single value (5): mean works (5), but stddev is rejected because it needs at least two.

**Validate before pandas:** pandas quietly skips missing values, which could change an answer without warning. So values go through numeric_values first, and a missing or bad value is rejected, not dropped. A quoted empty cell in a CSV becomes a missing value and fails this check; completely blank lines are skipped by pandas, which is fine.

**The path a CSV request takes:**
DataFrame (pd.read_csv reads the table) -> Series (frame["value"]) -> list (.tolist()) -> numeric tuple (Calculation runs numeric_values) -> stored operation (Calculation holds Operations.mean and the tuple; nothing runs yet) -> result (get_result() calls pandas and returns a float).

**Same answer from either source:** stddev 10 20 30 40 50 and csv stddev values.csv both give 15.8114, because after reading, both go through the same factory, checks, and math. My test test_csv_and_typed_values_match proves this with a second dataset.

**Why each part has its own home:**
- Math (statistics.py, Operations) only calculates; it doesn't know where the numbers came from.
- File reading (inputs.py) only gets the numbers out of the file; it does no math. A file is a source, not an operation.
- Construction (the factory) checks names, counts, and settings and builds the calculation.
- Display (commands and the CLI) turns results into text and handles errors.
Because they are separate, adding a new source (the CSV) didn't change the math, and the math can be tested without any files.

**EAFP vs. LBYL:** EAFP for number conversion and opening the file: just try it, and Python reports a clear error (I don't check that the file exists first, since it could still fail when read). LBYL for this app's own rules: the minimum number of values and the required value column are checked explicitly.