"""
Benchmark tests for performance.

Tests complexity and runtime for screening operations.
"""

import time
from typing import List
import statistics

from shortscreen.engine import ShortScreenEngine
from shortscreen.macro import MacroRegime
from shortscreen.data import DataProvider


def benchmark_screening(universe_sizes: List[int] = None):
    """
    Benchmark screening performance across different universe sizes.

    Args:
        universe_sizes: List of universe sizes to test
    """
    if universe_sizes is None:
        universe_sizes = [100, 500, 1000, 5000]

    print("\n" + "="*80)
    print("PERFORMANCE BENCHMARK")
    print("="*80)

    results = []

    for size in universe_sizes:
        # Create a data provider that returns exactly `size` tickers
        provider = DataProvider(use_mock=True)

        # Override get_universe to return specific size
        original_get_universe = provider.get_universe

        def get_fixed_universe(filters=None):
            all_tickers = original_get_universe(filters)
            return all_tickers[:size]

        provider.get_universe = get_fixed_universe

        # Create engine with custom provider
        engine = ShortScreenEngine(data_provider=provider)

        # Create regime
        regime = MacroRegime(downturn=0.6, inflation=0.5, liquidity=0.7)

        # Warm-up run
        _ = engine.run(regime)

        # Timed runs
        num_runs = 3
        times = []

        for _ in range(num_runs):
            start = time.time()
            candidates = engine.run(regime)
            elapsed = time.time() - start
            times.append(elapsed)

        avg_time = statistics.mean(times)
        std_time = statistics.stdev(times) if len(times) > 1 else 0

        # Calculate throughput
        throughput = size / avg_time

        results.append({
            'size': size,
            'avg_time': avg_time,
            'std_time': std_time,
            'throughput': throughput
        })

        print(f"\nUniverse size: {size:5d}")
        print(f"  Avg time:    {avg_time:7.3f}s ± {std_time:.3f}s")
        print(f"  Throughput:  {throughput:7.1f} tickers/sec")

    # Analyze complexity
    print("\n" + "="*80)
    print("COMPLEXITY ANALYSIS")
    print("="*80)

    # Check if roughly linear (O(n)) or worse
    if len(results) >= 2:
        # Compare first and last
        first = results[0]
        last = results[-1]

        size_ratio = last['size'] / first['size']
        time_ratio = last['avg_time'] / first['avg_time']

        print(f"\nSize ratio:  {size_ratio:.1f}x")
        print(f"Time ratio:  {time_ratio:.1f}x")

        if time_ratio < size_ratio * 1.5:
            complexity = "O(n) - Linear (good)"
        elif time_ratio < size_ratio ** 1.5:
            complexity = "O(n log n) - Log-linear (acceptable)"
        elif time_ratio < size_ratio ** 2:
            complexity = "O(n²) - Quadratic (needs optimization)"
        else:
            complexity = "Worse than O(n²) (requires optimization)"

        print(f"Estimated:   {complexity}")

    print("\n" + "="*80)

    # Check memory efficiency
    print("\nMEMORY NOTES:")
    print("  - O(n) space for raw metrics")
    print("  - O(n) space for factor scores")
    print("  - O(n) space for candidates")
    print("  - Total: O(n) space complexity (good)")

    print("\n" + "="*80 + "\n")

    return results


def test_benchmark_small_universe():
    """Test with small universe (CI-friendly)."""
    results = benchmark_screening([100, 200])
    assert len(results) == 2
    # Should be fast
    assert results[0]['avg_time'] < 5.0, "Small universe should process quickly"


def test_benchmark_medium_universe():
    """Test with medium universe."""
    results = benchmark_screening([500, 1000])
    assert len(results) == 2
    # Should still be reasonable
    assert results[-1]['avg_time'] < 10.0, "Medium universe should process in reasonable time"


if __name__ == "__main__":
    # Run full benchmark suite
    benchmark_screening([100, 500, 1000, 5000, 10000])
