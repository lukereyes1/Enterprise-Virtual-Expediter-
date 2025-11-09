"""
Main orchestration engine for short screening.

This module coordinates the entire screening process:
1. Build universe
2. Fetch raw metrics
3. Compute factor scores
4. Compute theme scores with macro-driven weights
5. Generate ranked short candidates
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import statistics

from shortscreen.data import DataProvider
from shortscreen.factors import (
    RawMetrics,
    FactorScores,
    compute_raw_metrics,
    compute_all_factor_scores
)
from shortscreen.themes import get_all_themes, compute_theme_scores
from shortscreen.macro import MacroRegime, compute_theme_weights, get_theme_name_mapping


@dataclass
class ShortCandidate:
    """
    A short candidate with all relevant scores and metadata.
    """
    ticker: str
    global_vulnerability_score: float
    dominant_theme: str
    dominant_theme_score: float

    # Individual theme scores
    theme_scores: Dict[str, float]

    # Factor scores
    valuation_score: float
    profitability_score: float
    growth_score: float
    leverage_score: float
    quality_score: float
    market_score: float

    # Key raw metrics
    market_cap: float
    sector: str
    revenue_growth: float
    net_margin: float
    debt_to_equity: float
    beta: float


class ShortScreenEngine:
    """
    Main engine for running the short screening process.
    """

    def __init__(self, data_provider: Optional[DataProvider] = None):
        """
        Initialize the screening engine.

        Args:
            data_provider: Optional DataProvider instance. If None, creates default.
        """
        self.data_provider = data_provider or DataProvider(use_mock=True)
        self.themes = get_all_themes()
        self.theme_name_mapping = get_theme_name_mapping()

    def run(
        self,
        macro_regime: MacroRegime,
        universe_filters: Optional[Dict] = None,
        min_candidates: int = 20
    ) -> List[ShortCandidate]:
        """
        Run the complete screening process.

        Args:
            macro_regime: Current macro regime indicators
            universe_filters: Optional filters for universe selection
            min_candidates: Minimum number of candidates to return

        Returns:
            Sorted list of ShortCandidate objects (highest score first)
        """
        # Step 1: Build universe
        universe_tickers = self.data_provider.get_universe(universe_filters)

        # Step 2: Fetch raw data
        market_data_map = self.data_provider.get_batch_market_data(universe_tickers)
        fundamental_data_map = self.data_provider.get_batch_fundamental_data(universe_tickers)

        # Step 3: Compute raw metrics for all tickers
        universe_metrics: List[RawMetrics] = []
        for ticker in universe_tickers:
            market_data = market_data_map.get(ticker)
            fundamental_data = fundamental_data_map.get(ticker)

            if market_data and fundamental_data:
                raw_metrics = compute_raw_metrics(ticker, market_data, fundamental_data)
                universe_metrics.append(raw_metrics)

        # Step 4: Compute factor scores
        factor_scores_map = compute_all_factor_scores(universe_metrics)

        # Step 5: Compute theme weights based on macro regime
        theme_weights = compute_theme_weights(macro_regime)

        # Step 6: Compute global vulnerability scores
        candidates = []
        for raw_metrics in universe_metrics:
            ticker = raw_metrics.ticker
            factor_scores = factor_scores_map[ticker]

            # Compute theme scores
            theme_scores = compute_theme_scores(ticker, factor_scores, raw_metrics)

            # Compute global vulnerability score as weighted sum of theme scores
            global_score = self._compute_global_score(theme_scores, theme_weights)

            # Find dominant theme (theme with highest score)
            dominant_theme, dominant_score = self._get_dominant_theme(theme_scores)

            # Create candidate
            candidate = ShortCandidate(
                ticker=ticker,
                global_vulnerability_score=global_score,
                dominant_theme=dominant_theme,
                dominant_theme_score=dominant_score,
                theme_scores=theme_scores,
                valuation_score=factor_scores.valuation_score,
                profitability_score=factor_scores.profitability_score,
                growth_score=factor_scores.growth_score,
                leverage_score=factor_scores.leverage_score,
                quality_score=factor_scores.quality_score,
                market_score=factor_scores.market_score,
                market_cap=raw_metrics.market_cap,
                sector=raw_metrics.sector,
                revenue_growth=raw_metrics.revenue_growth,
                net_margin=raw_metrics.net_margin,
                debt_to_equity=raw_metrics.debt_to_equity,
                beta=raw_metrics.beta
            )
            candidates.append(candidate)

        # Step 7: Sort by global vulnerability score (descending)
        candidates.sort(key=lambda x: x.global_vulnerability_score, reverse=True)

        return candidates

    def _compute_global_score(
        self,
        theme_scores: Dict[str, float],
        theme_weights: Dict[str, float]
    ) -> float:
        """
        Compute global vulnerability score as weighted sum of theme scores.

        Args:
            theme_scores: Dictionary of theme scores (display names)
            theme_weights: Dictionary of theme weights (config keys)

        Returns:
            Weighted global score (0-100)
        """
        total_score = 0.0
        for config_key, weight in theme_weights.items():
            display_name = self.theme_name_mapping.get(config_key, config_key)
            theme_score = theme_scores.get(display_name, 0.0)
            total_score += weight * theme_score

        return total_score

    def _get_dominant_theme(self, theme_scores: Dict[str, float]) -> tuple[str, float]:
        """
        Find the theme with the highest score.

        Args:
            theme_scores: Dictionary mapping theme names to scores

        Returns:
            Tuple of (theme_name, score)
        """
        if not theme_scores:
            return ("None", 0.0)

        dominant_theme = max(theme_scores.items(), key=lambda x: x[1])
        return dominant_theme

    def get_statistics(self, candidates: List[ShortCandidate]) -> Dict:
        """
        Compute statistics about the candidate list.

        Args:
            candidates: List of ShortCandidate objects

        Returns:
            Dictionary with statistics
        """
        if not candidates:
            return {}

        return {
            'total_candidates': len(candidates),
            'avg_global_score': statistics.mean(c.global_vulnerability_score for c in candidates),
            'median_global_score': statistics.median(c.global_vulnerability_score for c in candidates),
            'sector_distribution': self._compute_sector_distribution(candidates),
            'dominant_theme_distribution': self._compute_theme_distribution(candidates),
            'avg_market_cap': statistics.mean(c.market_cap for c in candidates),
        }

    def _compute_sector_distribution(self, candidates: List[ShortCandidate]) -> Dict[str, int]:
        """Compute distribution of candidates by sector."""
        distribution = {}
        for candidate in candidates:
            distribution[candidate.sector] = distribution.get(candidate.sector, 0) + 1
        return distribution

    def _compute_theme_distribution(self, candidates: List[ShortCandidate]) -> Dict[str, int]:
        """Compute distribution of candidates by dominant theme."""
        distribution = {}
        for candidate in candidates:
            theme = candidate.dominant_theme
            distribution[theme] = distribution.get(theme, 0) + 1
        return distribution
