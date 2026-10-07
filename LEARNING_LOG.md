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