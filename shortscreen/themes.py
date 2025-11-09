"""
Theme classes for short screening.

This module defines the four investment themes, each with methods to:
- filter_universe: Filter tickers that match the theme criteria
- score: Compute a theme-specific score for a ticker
- etf_proxies: Return ETF tickers that represent the theme
"""

from abc import ABC, abstractmethod
from typing import List, Dict
import statistics
import yaml

from shortscreen.factors import RawMetrics, FactorScores
from shortscreen.config import ETF_PROXIES_PATH


class Theme(ABC):
    """Abstract base class for investment themes."""

    def __init__(self):
        """Initialize theme with ETF proxies from config."""
        self._etf_proxies = self._load_etf_proxies()

    @abstractmethod
    def filter_universe(self, raw_metrics: RawMetrics) -> bool:
        """
        Filter tickers that match this theme's criteria.

        Args:
            raw_metrics: Raw metrics for a ticker

        Returns:
            True if ticker matches theme criteria, False otherwise
        """
        pass

    @abstractmethod
    def score(self, factor_scores: FactorScores, raw_metrics: RawMetrics) -> float:
        """
        Compute a theme-specific vulnerability score.

        Args:
            factor_scores: Factor scores for the ticker
            raw_metrics: Raw metrics for the ticker

        Returns:
            Theme score (0-100, higher = more vulnerable)
        """
        pass

    @abstractmethod
    def theme_name(self) -> str:
        """Return the theme name."""
        pass

    def etf_proxies(self) -> List[str]:
        """
        Return ETF tickers that represent this theme.

        Returns:
            List of ETF ticker symbols
        """
        return self._etf_proxies.get(self._get_config_key(), [])

    @abstractmethod
    def _get_config_key(self) -> str:
        """Return the config key for this theme."""
        pass

    def _load_etf_proxies(self) -> Dict[str, List[str]]:
        """Load ETF proxies from config file."""
        try:
            with open(ETF_PROXIES_PATH, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('proxies', {})
        except Exception as e:
            print(f"Warning: Could not load ETF proxies: {e}")
            return {}


class UnprofitableGrowthTheme(Theme):
    """
    Unprofitable Growth Theme.

    Targets high-growth, unprofitable companies that are vulnerable to:
    - Valuation compression
    - Profitability concerns
    - Growth deceleration
    """

    def theme_name(self) -> str:
        return "Unprofitable Growth"

    def _get_config_key(self) -> str:
        return "unprofitable_growth"

    def filter_universe(self, raw_metrics: RawMetrics) -> bool:
        """
        Filter for unprofitable growth stocks.

        Criteria:
        - High revenue growth (>15%)
        - Negative or low net margin (<5%)
        - High valuation (P/S > 3)
        """
        return (
            raw_metrics.revenue_growth > 0.15 and
            raw_metrics.net_margin < 0.05 and
            raw_metrics.price_to_sales > 3.0
        )

    def score(self, factor_scores: FactorScores, raw_metrics: RawMetrics) -> float:
        """
        Score based on valuation, profitability, and growth deceleration risk.

        Higher weight on:
        - Valuation (40%)
        - Profitability (40%)
        - Growth sustainability (20%)
        """
        return (
            0.40 * factor_scores.valuation_score +
            0.40 * factor_scores.profitability_score +
            0.20 * factor_scores.growth_score
        )


class OverLeveredSmallCapsTheme(Theme):
    """
    Over-Leveraged Small Caps Theme.

    Targets small-cap companies with high debt loads that are vulnerable to:
    - Refinancing risk
    - Liquidity stress
    - Credit downgrades
    """

    def theme_name(self) -> str:
        return "Over-Leveraged Small Caps"

    def _get_config_key(self) -> str:
        return "overleveraged_smallcaps"

    def filter_universe(self, raw_metrics: RawMetrics) -> bool:
        """
        Filter for over-leveraged small caps.

        Criteria:
        - Market cap < $2B
        - High debt-to-equity (>1.5)
        - Net debt / EBITDA > 3
        """
        return (
            raw_metrics.market_cap < 2000 and  # $2B
            raw_metrics.debt_to_equity > 1.5 and
            raw_metrics.net_debt_to_ebitda > 3.0
        )

    def score(self, factor_scores: FactorScores, raw_metrics: RawMetrics) -> float:
        """
        Score based on leverage, quality, and market cap.

        Higher weight on:
        - Leverage (50%)
        - Quality/liquidity (30%)
        - Market dynamics (20%)
        """
        return (
            0.50 * factor_scores.leverage_score +
            0.30 * factor_scores.quality_score +
            0.20 * factor_scores.market_score
        )


class HighBetaConsumerTheme(Theme):
    """
    High Beta Consumer Theme.

    Targets consumer discretionary stocks with high beta that are vulnerable to:
    - Economic downturn
    - Consumer spending slowdown
    - High sensitivity to market moves
    """

    def theme_name(self) -> str:
        return "High Beta Consumer"

    def _get_config_key(self) -> str:
        return "highbeta_consumer"

    def filter_universe(self, raw_metrics: RawMetrics) -> bool:
        """
        Filter for high beta consumer stocks.

        Criteria:
        - Consumer Discretionary sector
        - Beta > 1.3
        - Revenue growth positive (not in secular decline)
        """
        return (
            raw_metrics.sector == "Consumer Discretionary" and
            raw_metrics.beta > 1.3 and
            raw_metrics.revenue_growth > -0.05
        )

    def score(self, factor_scores: FactorScores, raw_metrics: RawMetrics) -> float:
        """
        Score based on market sensitivity, profitability, and valuation.

        Higher weight on:
        - Market risk (40%)
        - Profitability (30%)
        - Valuation (30%)
        """
        return (
            0.40 * factor_scores.market_score +
            0.30 * factor_scores.profitability_score +
            0.30 * factor_scores.valuation_score
        )


class WeakFinancialsTheme(Theme):
    """
    Weak Financials Theme.

    Targets financial companies with weak fundamentals that are vulnerable to:
    - Credit quality deterioration
    - Capital adequacy concerns
    - Regulatory stress
    """

    def theme_name(self) -> str:
        return "Weak Financials"

    def _get_config_key(self) -> str:
        return "weak_financials"

    def filter_universe(self, raw_metrics: RawMetrics) -> bool:
        """
        Filter for weak financial stocks.

        Criteria:
        - Financials sector
        - Low ROE (<8%)
        - High leverage or low quality (negative FCF or low current ratio)
        """
        return (
            raw_metrics.sector == "Financials" and
            raw_metrics.roe < 0.08 and
            (raw_metrics.debt_to_assets > 0.7 or raw_metrics.fcf_margin < 0.0)
        )

    def score(self, factor_scores: FactorScores, raw_metrics: RawMetrics) -> float:
        """
        Score based on profitability, quality, and leverage.

        Higher weight on:
        - Profitability (40%)
        - Quality (35%)
        - Leverage (25%)
        """
        return (
            0.40 * factor_scores.profitability_score +
            0.35 * factor_scores.quality_score +
            0.25 * factor_scores.leverage_score
        )


def get_all_themes() -> List[Theme]:
    """
    Return all available themes.

    Returns:
        List of Theme instances
    """
    return [
        UnprofitableGrowthTheme(),
        OverLeveredSmallCapsTheme(),
        HighBetaConsumerTheme(),
        WeakFinancialsTheme()
    ]


def compute_theme_scores(
    ticker: str,
    factor_scores: FactorScores,
    raw_metrics: RawMetrics
) -> Dict[str, float]:
    """
    Compute scores for all themes for a given ticker.

    Args:
        ticker: Stock ticker symbol
        factor_scores: Factor scores for the ticker
        raw_metrics: Raw metrics for the ticker

    Returns:
        Dictionary mapping theme names to scores (0-100)
    """
    themes = get_all_themes()
    scores = {}

    for theme in themes:
        if theme.filter_universe(raw_metrics):
            scores[theme.theme_name()] = theme.score(factor_scores, raw_metrics)
        else:
            scores[theme.theme_name()] = 0.0

    return scores
