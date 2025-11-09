"""
Regression tests for stable rankings.

These tests ensure that the screening engine produces stable, reproducible
results for a fixed universe of synthetic tickers.
"""

import pytest
import json
from pathlib import Path
from typing import List

from shortscreen.engine import ShortScreenEngine, ShortCandidate
from shortscreen.macro import MacroRegime


# Fixed seed for reproducible mock data
REGRESSION_SEED = 42

# Path to store baseline rankings
BASELINE_PATH = Path(__file__).parent / "fixtures" / "baseline_rankings.json"


def get_baseline_macro_regime() -> MacroRegime:
    """Get baseline macro regime for regression tests."""
    return MacroRegime(
        downturn=0.6,
        inflation=0.5,
        liquidity=0.7
    )


def run_screening_engine() -> List[ShortCandidate]:
    """Run the screening engine with fixed settings."""
    engine = ShortScreenEngine()
    regime = get_baseline_macro_regime()
    candidates = engine.run(regime)
    return candidates


def extract_ranking(candidates: List[ShortCandidate]) -> dict:
    """
    Extract ranking data for comparison.

    Returns a dict with:
    - tickers: List of tickers in ranked order
    - scores: List of global scores
    - themes: List of dominant themes
    """
    return {
        'tickers': [c.ticker for c in candidates],
        'scores': [round(c.global_vulnerability_score, 2) for c in candidates],
        'themes': [c.dominant_theme for c in candidates]
    }


def save_baseline(candidates: List[ShortCandidate]):
    """Save baseline rankings to file."""
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ranking = extract_ranking(candidates)

    with open(BASELINE_PATH, 'w') as f:
        json.dump(ranking, f, indent=2)

    print(f"Baseline saved to {BASELINE_PATH}")


def load_baseline() -> dict:
    """Load baseline rankings from file."""
    if not BASELINE_PATH.exists():
        return None

    with open(BASELINE_PATH, 'r') as f:
        return json.load(f)


def compare_rankings(current: dict, baseline: dict, tolerance: float = 0.01) -> tuple[bool, str]:
    """
    Compare current rankings with baseline.

    Args:
        current: Current ranking data
        baseline: Baseline ranking data
        tolerance: Tolerance for score differences

    Returns:
        Tuple of (is_stable, message)
    """
    issues = []

    # Check if same number of candidates
    if len(current['tickers']) != len(baseline['tickers']):
        issues.append(
            f"Different number of candidates: {len(current['tickers'])} vs {len(baseline['tickers'])}"
        )

    # Check top 20 tickers match
    top_n = min(20, len(current['tickers']), len(baseline['tickers']))
    current_top_20 = current['tickers'][:top_n]
    baseline_top_20 = baseline['tickers'][:top_n]

    if current_top_20 != baseline_top_20:
        # Find differences
        for i in range(top_n):
            if current_top_20[i] != baseline_top_20[i]:
                issues.append(
                    f"Rank {i+1}: {current_top_20[i]} (current) vs {baseline_top_20[i]} (baseline)"
                )

    # Check scores are within tolerance
    for i in range(top_n):
        ticker = current['tickers'][i]
        current_score = current['scores'][i]
        baseline_score = baseline['scores'][i]

        diff = abs(current_score - baseline_score)
        if diff > tolerance:
            issues.append(
                f"{ticker}: score changed by {diff:.3f} ({current_score:.2f} vs {baseline_score:.2f})"
            )

    if issues:
        message = "Rankings changed:\n" + "\n".join(f"  - {issue}" for issue in issues)
        return False, message
    else:
        return True, "Rankings are stable within tolerance"


class TestRegressionStability:
    """Regression tests for ranking stability."""

    def test_rankings_are_stable(self):
        """Test that rankings remain stable across runs."""
        # Run current screening
        candidates = run_screening_engine()
        current_ranking = extract_ranking(candidates)

        # Load baseline
        baseline = load_baseline()

        if baseline is None:
            # First run - save as baseline
            save_baseline(candidates)
            pytest.skip("Baseline not found - saved current run as baseline")

        # Compare with baseline
        is_stable, message = compare_rankings(current_ranking, baseline)

        print(f"\nRegression test result:")
        print(message)

        if not is_stable:
            print("\n⚠️  Rankings have changed!")
            print("If this change is intentional (model improvement), update baseline with:")
            print(f"  python -m tests.test_regression --update-baseline")

        assert is_stable, message

    def test_macro_regime_changes_affect_rankings(self):
        """Test that different macro regimes produce different rankings."""
        # Baseline regime
        engine = ShortScreenEngine()
        baseline_regime = MacroRegime(downturn=0.5, inflation=0.5, liquidity=0.5)
        baseline_candidates = engine.run(baseline_regime)

        # High stress regime
        stress_regime = MacroRegime(downturn=0.9, inflation=0.9, liquidity=0.9)
        stress_candidates = engine.run(stress_regime)

        # Rankings should be different
        baseline_top_10 = [c.ticker for c in baseline_candidates[:10]]
        stress_top_10 = [c.ticker for c in stress_candidates[:10]]

        # At least some difference in top 10
        differences = sum(1 for i in range(10) if baseline_top_10[i] != stress_top_10[i])

        print(f"\nMacro sensitivity test:")
        print(f"  Baseline top 10: {baseline_top_10[:5]}...")
        print(f"  Stress top 10:   {stress_top_10[:5]}...")
        print(f"  Differences in top 10: {differences}/10")

        # Should have some differences (model is responsive to macro)
        assert differences > 0, "Rankings should change with macro regime"


def update_baseline():
    """CLI tool to update baseline rankings."""
    print("Updating baseline rankings...")
    candidates = run_screening_engine()
    save_baseline(candidates)
    print("✓ Baseline updated successfully")


if __name__ == "__main__":
    import sys

    if "--update-baseline" in sys.argv:
        update_baseline()
    else:
        # Run tests
        test = TestRegressionStability()
        print("\nRunning regression tests...\n")

        try:
            test.test_rankings_are_stable()
        except Exception as e:
            print(f"\n❌ Stability test failed: {e}")

        test.test_macro_regime_changes_affect_rankings()

        print("\n✓ Regression tests complete")
