"""Shared statistics policy: mean and standard deviation with pandas."""

from math import isfinite

import numpy as np
import pandas as pd

from calculator.validation import numeric_values


def mean(values) -> float:
    numbers = numeric_values(values)        # validate first: no silent dropping
    if not numbers:
        raise ValueError("Enter at least one value.")
    with np.errstate(over="ignore", invalid="ignore"):   # overflow is checked below
        result = float(pd.Series(numbers, dtype=float).mean())
    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")
    return result


def standard_deviation(values, *, ddof=1) -> float:
    """Default ddof=1 is sample deviation; ddof=0 is population deviation."""
    if ddof not in (0, 1):
        raise ValueError("ddof must be 0 (population) or 1 (sample).")
    numbers = numeric_values(values)
    if len(numbers) < 2:
        raise ValueError("Enter at least two values.")
    with np.errstate(over="ignore", invalid="ignore"):
        result = float(pd.Series(numbers, dtype=float).std(ddof=int(ddof)))
    if not isfinite(result):
        raise ValueError("Result is outside the supported range.")
    return result