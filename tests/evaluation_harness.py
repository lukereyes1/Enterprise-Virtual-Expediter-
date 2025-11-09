"""
Evaluation harness for model quality assessment.

This harness computes diagnostic metrics on screening results:
- Factor distributions
- Sector concentrations
- Theme distributions
- Ranking stability over time
- Performance metrics (when historical data is available)
"""

import json
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
import statistics

from shortscreen.engine import ShortScreenEngine, ShortCandidate
from shortscreen.macro import MacroRegime


@dataclass
class EvaluationMetrics:
    """Container for evaluation metrics."""
    # Basic statistics
    total_candidates: int
    avg_global_score: float
    median_global_score: float
    score_std_dev: float

    # Distributions
    sector_distribution: Dict[str, int]
    theme_distribution: Dict[str, int]
    sector_concentration: float  # Herfindahl index

    # Top candidates analysis
    top_20_avg_score: float
    top_20_sectors: Dict[str, int]
    top_20_themes: Dict[str, int]

    # Factor score statistics (top 20)
    avg_valuation_score: float
    avg_profitability_score: float
    avg_leverage_score: float
    avg_quality_score: float
    avg_growth_score: float
    avg_market_score: float


class EvaluationHarness:
    """
    Evaluation harness for assessing model quality.

    This harness runs the screening engine and computes diagnostic metrics
    to help evaluate model behavior and detect regressions.
    """

    def __init__(self):
        """Initialize the evaluation harness."""
        self.engine = ShortScreenEngine()
        self.results_dir = Path(__file__).parent / "evaluation_results"
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def run_evaluation(
        self,
        macro_regime: MacroRegime,
        name: str = "evaluation"
    ) -> EvaluationMetrics:
        """
        Run evaluation on a macro regime.

        Args:
            macro_regime: Macro regime to evaluate
            name: Name for this evaluation run

        Returns:
            EvaluationMetrics object
        """
        # Run screening
        candidates = self.engine.run(macro_regime)

        # Compute metrics
        metrics = self._compute_metrics(candidates)

        # Save results
        self._save_results(metrics, name, macro_regime)

        return metrics

    def compare_evaluations(
        self,
        name_a: str,
        name_b: str
    ) -> Dict:
        """
        Compare two evaluation runs.

        Args:
            name_a: Name of first evaluation
            name_b: Name of second evaluation

        Returns:
            Dictionary with comparison results
        """
        metrics_a = self._load_results(name_a)
        metrics_b = self._load_results(name_b)

        if not metrics_a or not metrics_b:
            return {"error": "One or both evaluations not found"}

        comparison = {
            "score_delta": metrics_b['avg_global_score'] - metrics_a['avg_global_score'],
            "concentration_delta": metrics_b['sector_concentration'] - metrics_a['sector_concentration'],
            "top_20_score_delta": metrics_b['top_20_avg_score'] - metrics_a['top_20_avg_score'],
            "sector_shift": self._compute_distribution_shift(
                metrics_a['sector_distribution'],
                metrics_b['sector_distribution']
            ),
            "theme_shift": self._compute_distribution_shift(
                metrics_a['theme_distribution'],
                metrics_b['theme_distribution']
            )
        }

        return comparison

    def _compute_metrics(self, candidates: List[ShortCandidate]) -> EvaluationMetrics:
        """Compute evaluation metrics from candidates."""
        if not candidates:
            raise ValueError("No candidates to evaluate")

        # Basic statistics
        scores = [c.global_vulnerability_score for c in candidates]
        total_candidates = len(candidates)
        avg_global_score = statistics.mean(scores)
        median_global_score = statistics.median(scores)
        score_std_dev = statistics.stdev(scores) if len(scores) > 1 else 0.0

        # Sector distribution
        sector_dist = {}
        for c in candidates:
            sector_dist[c.sector] = sector_dist.get(c.sector, 0) + 1

        # Theme distribution
        theme_dist = {}
        for c in candidates:
            theme_dist[c.dominant_theme] = theme_dist.get(c.dominant_theme, 0) + 1

        # Sector concentration (Herfindahl index)
        sector_shares = [count / total_candidates for count in sector_dist.values()]
        sector_concentration = sum(share ** 2 for share in sector_shares)

        # Top 20 analysis
        top_20 = candidates[:min(20, len(candidates))]
        top_20_scores = [c.global_vulnerability_score for c in top_20]
        top_20_avg_score = statistics.mean(top_20_scores)

        top_20_sectors = {}
        top_20_themes = {}
        for c in top_20:
            top_20_sectors[c.sector] = top_20_sectors.get(c.sector, 0) + 1
            top_20_themes[c.dominant_theme] = top_20_themes.get(c.dominant_theme, 0) + 1

        # Average factor scores (top 20)
        avg_valuation = statistics.mean(c.valuation_score for c in top_20)
        avg_profitability = statistics.mean(c.profitability_score for c in top_20)
        avg_leverage = statistics.mean(c.leverage_score for c in top_20)
        avg_quality = statistics.mean(c.quality_score for c in top_20)
        avg_growth = statistics.mean(c.growth_score for c in top_20)
        avg_market = statistics.mean(c.market_score for c in top_20)

        return EvaluationMetrics(
            total_candidates=total_candidates,
            avg_global_score=avg_global_score,
            median_global_score=median_global_score,
            score_std_dev=score_std_dev,
            sector_distribution=sector_dist,
            theme_distribution=theme_dist,
            sector_concentration=sector_concentration,
            top_20_avg_score=top_20_avg_score,
            top_20_sectors=top_20_sectors,
            top_20_themes=top_20_themes,
            avg_valuation_score=avg_valuation,
            avg_profitability_score=avg_profitability,
            avg_leverage_score=avg_leverage,
            avg_quality_score=avg_quality,
            avg_growth_score=avg_growth,
            avg_market_score=avg_market
        )

    def _save_results(self, metrics: EvaluationMetrics, name: str, regime: MacroRegime):
        """Save evaluation results to file."""
        result = {
            'name': name,
            'macro_regime': {
                'downturn': regime.downturn,
                'inflation': regime.inflation,
                'liquidity': regime.liquidity
            },
            'total_candidates': metrics.total_candidates,
            'avg_global_score': round(metrics.avg_global_score, 2),
            'median_global_score': round(metrics.median_global_score, 2),
            'score_std_dev': round(metrics.score_std_dev, 2),
            'sector_distribution': metrics.sector_distribution,
            'theme_distribution': metrics.theme_distribution,
            'sector_concentration': round(metrics.sector_concentration, 3),
            'top_20_avg_score': round(metrics.top_20_avg_score, 2),
            'top_20_sectors': metrics.top_20_sectors,
            'top_20_themes': metrics.top_20_themes,
            'factor_scores': {
                'valuation': round(metrics.avg_valuation_score, 2),
                'profitability': round(metrics.avg_profitability_score, 2),
                'leverage': round(metrics.avg_leverage_score, 2),
                'quality': round(metrics.avg_quality_score, 2),
                'growth': round(metrics.avg_growth_score, 2),
                'market': round(metrics.avg_market_score, 2)
            }
        }

        output_path = self.results_dir / f"{name}.json"
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"Results saved to {output_path}")

    def _load_results(self, name: str) -> Dict:
        """Load evaluation results from file."""
        path = self.results_dir / f"{name}.json"
        if not path.exists():
            return None

        with open(path, 'r') as f:
            return json.load(f)

    def _compute_distribution_shift(self, dist_a: Dict, dist_b: Dict) -> float:
        """
        Compute total variation distance between two distributions.

        Returns a value between 0 (identical) and 1 (completely different).
        """
        all_keys = set(dist_a.keys()) | set(dist_b.keys())
        total_a = sum(dist_a.values())
        total_b = sum(dist_b.values())

        shift = 0.0
        for key in all_keys:
            prob_a = dist_a.get(key, 0) / total_a if total_a > 0 else 0
            prob_b = dist_b.get(key, 0) / total_b if total_b > 0 else 0
            shift += abs(prob_a - prob_b)

        return shift / 2.0  # Normalize to [0, 1]

    def print_metrics(self, metrics: EvaluationMetrics):
        """Print evaluation metrics in a readable format."""
        print("\n" + "="*80)
        print("EVALUATION METRICS")
        print("="*80)

        print(f"\nOverall Statistics:")
        print(f"  Total Candidates:     {metrics.total_candidates}")
        print(f"  Avg Global Score:     {metrics.avg_global_score:.2f}")
        print(f"  Median Global Score:  {metrics.median_global_score:.2f}")
        print(f"  Score Std Dev:        {metrics.score_std_dev:.2f}")
        print(f"  Sector Concentration: {metrics.sector_concentration:.3f}")

        print(f"\nTop 20 Analysis:")
        print(f"  Average Score:        {metrics.top_20_avg_score:.2f}")

        print(f"\n  Sector Distribution:")
        for sector, count in sorted(metrics.top_20_sectors.items(), key=lambda x: -x[1])[:5]:
            pct = 100 * count / sum(metrics.top_20_sectors.values())
            print(f"    {sector:30s}: {count:2d} ({pct:5.1f}%)")

        print(f"\n  Theme Distribution:")
        for theme, count in sorted(metrics.top_20_themes.items(), key=lambda x: -x[1]):
            pct = 100 * count / sum(metrics.top_20_themes.values())
            print(f"    {theme:30s}: {count:2d} ({pct:5.1f}%)")

        print(f"\n  Average Factor Scores:")
        print(f"    Valuation:     {metrics.avg_valuation_score:.2f}")
        print(f"    Profitability: {metrics.avg_profitability_score:.2f}")
        print(f"    Leverage:      {metrics.avg_leverage_score:.2f}")
        print(f"    Quality:       {metrics.avg_quality_score:.2f}")
        print(f"    Growth:        {metrics.avg_growth_score:.2f}")
        print(f"    Market:        {metrics.avg_market_score:.2f}")

        print("="*80)


def main():
    """Run evaluation harness."""
    harness = EvaluationHarness()

    # Define test regimes
    regimes = {
        'baseline': MacroRegime(downturn=0.5, inflation=0.5, liquidity=0.5),
        'stress': MacroRegime(downturn=0.9, inflation=0.8, liquidity=0.8),
        'benign': MacroRegime(downturn=0.2, inflation=0.3, liquidity=0.2),
    }

    print("\nRunning evaluation harness across multiple macro regimes...\n")

    # Run evaluations
    results = {}
    for name, regime in regimes.items():
        print(f"\nEvaluating {name} regime...")
        metrics = harness.run_evaluation(regime, name)
        results[name] = metrics
        harness.print_metrics(metrics)

    # Compare regimes
    print("\n" + "="*80)
    print("REGIME COMPARISONS")
    print("="*80)

    print("\nBaseline vs Stress:")
    comparison = harness.compare_evaluations('baseline', 'stress')
    print(f"  Score Delta:         {comparison['score_delta']:+.2f}")
    print(f"  Top 20 Score Delta:  {comparison['top_20_score_delta']:+.2f}")
    print(f"  Sector Shift:        {comparison['sector_shift']:.3f}")
    print(f"  Theme Shift:         {comparison['theme_shift']:.3f}")

    print("\nBaseline vs Benign:")
    comparison = harness.compare_evaluations('baseline', 'benign')
    print(f"  Score Delta:         {comparison['score_delta']:+.2f}")
    print(f"  Top 20 Score Delta:  {comparison['top_20_score_delta']:+.2f}")
    print(f"  Sector Shift:        {comparison['sector_shift']:.3f}")
    print(f"  Theme Shift:         {comparison['theme_shift']:.3f}")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
