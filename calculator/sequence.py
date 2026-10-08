"""Guided transfer: process already prepared calculations independently.

CSV request parsing and batch-specific commands are assessment adaptations.
This example deliberately receives Calculation objects, not file rows.
"""


def execute_sequence(session, calculations):
    results = []
    errors = []
    for calculation in calculations:
        try:                                    # one try per item: a failure only affects that item
            result = session.calculate(calculation)
        except (ValueError, ZeroDivisionError, OverflowError) as error:
            errors.append(str(error))
        else:                                   # runs only after success
            results.append(result)
    return results, errors