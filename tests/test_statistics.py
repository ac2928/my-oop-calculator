"""Statistics follow this application's own rules, checked before pandas runs."""

import pytest

from calculator.factory import CalculationFactory
from calculator.statistics import mean, standard_deviation


def test_mean():
    assert mean([2, 4, 6]) == 4.0


def test_mean_of_one_value():
    assert mean([5]) == 5.0     # one observation is enough for a mean


def test_mean_needs_at_least_one_value():
    with pytest.raises(ValueError, match="at least one"):
        mean([])


def test_sample_deviation_is_the_default():
    assert standard_deviation([2, 4, 6]) == pytest.approx(2.0)


def test_population_deviation_with_ddof_0():
    assert standard_deviation([2, 4, 6], ddof=0) == pytest.approx(1.6330, abs=1e-4)


def test_identical_values_have_zero_deviation():
    assert standard_deviation([7, 7, 7]) == 0.0


@pytest.mark.parametrize("ddof", [0, 1])
def test_deviation_needs_two_values_for_both_settings(ddof):
    with pytest.raises(ValueError, match="at least two"):
        standard_deviation([5], ddof=ddof)


@pytest.mark.parametrize("ddof", [2, -1, 0.5])
def test_unsupported_ddof_is_rejected(ddof):
    with pytest.raises(ValueError, match="ddof must be 0"):
        standard_deviation([1, 2, 3], ddof=ddof)


def test_missing_or_nonnumeric_values_are_rejected_not_dropped():
    with pytest.raises(ValueError, match="numeric"):
        mean(["a", 1])
    with pytest.raises(ValueError, match="finite"):
        standard_deviation([1, float("nan"), 3])


def test_nonfinite_results_are_rejected():
    with pytest.raises(ValueError, match="outside the supported range"):
        mean([1e308, 1e308])
    with pytest.raises(ValueError, match="outside the supported range"):
        standard_deviation([-1e308, 1e308])


def test_factory_builds_mean_and_stddev():
    assert CalculationFactory.create("mean", 10, 20, 30, 40, 50).get_result() == 30.0
    calculation = CalculationFactory.create("stddev", 10, 20, 30, 40, 50)
    assert calculation.get_result() == pytest.approx(15.8114, abs=1e-4)


def test_factory_passes_ddof_as_a_setting():
    calculation = CalculationFactory.create("stddev", 2, 4, 6, ddof="0")
    assert calculation.options == {"ddof": 0.0}
    assert calculation.get_result() == pytest.approx(1.6330, abs=1e-4)


def test_ddof_is_only_allowed_for_stddev():
    with pytest.raises(ValueError, match="Unsupported option for mean: ddof"):
        CalculationFactory.create("mean", 1, 2, ddof=0)