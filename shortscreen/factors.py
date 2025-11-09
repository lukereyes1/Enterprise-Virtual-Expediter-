"""
Factor computation module for short screening.

This module defines raw metrics, factor scores, and the logic to compute
percentile-based factor scores across a universe of stocks.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import statistics

from shortscreen.data import MarketData, FundamentalData


@dataclass
class RawMetrics:
    """
    Raw financial and market metrics for a ticker.

    These metrics are computed from market and fundamental data and serve
    as inputs to factor score calculations.
    """
    ticker: str

    # Valuation metrics
    price_to_sales: float
    price_to_book: float
    ev_to_ebitda: float

    # Profitability metrics
    net_margin: float
    ebitda_margin: float
    roe: float  # Return on Equity

    # Growth metrics
    revenue_growth: float

    # Leverage metrics
    debt_to_equity: float
    debt_to_assets: float
    net_debt_to_ebitda: float

    # Quality metrics
    fcf_margin: float
    current_ratio: float

    # Market metrics
    beta: float
    market_cap: float
    distance_from_52w_high: float  # (52w_high - price) / price

    # Sector/Industry
    sector: str
    industry: str


@dataclass
class FactorScores:
    """
    Percentile-based factor scores for a ticker.

    Each score is a percentile rank (0-100) where higher values indicate
    more bearish characteristics for that factor.
    """
    ticker: str

    # Valuation scores (higher = more expensive = more bearish)
    valuation_score: float

    # Profitability scores (higher = less profitable = more bearish)
    profitability_score: float

    # Growth scores (higher = negative/slowing growth = more bearish)
    growth_score: float

    # Leverage scores (higher = more levered = more bearish)
    leverage_score: float

    # Quality scores (higher = lower quality = more bearish)
    quality_score: float

    # Market scores (higher = higher beta/momentum issues = more bearish)
    market_score: float


def compute_raw_metrics(
    ticker: str,
    market_data: MarketData,
    fundamental_data: FundamentalData
) -> RawMetrics:
    """
    Compute raw metrics from market and fundamental data.

    Args:
        ticker: Stock ticker symbol
        market_data: Market data for the ticker
        fundamental_data: Fundamental data for the ticker

    Returns:
        RawMetrics object with computed metrics
    """
    # Safely compute ratios with division by zero protection
    def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
        return numerator / denominator if denominator != 0 else default

    # Valuation metrics
    market_cap_actual = market_data.market_cap
    price_to_sales = safe_divide(market_cap_actual, fundamental_data.revenue)
    price_to_book = safe_divide(market_cap_actual, fundamental_data.total_equity)

    enterprise_value = market_cap_actual + fundamental_data.total_debt - fundamental_data.cash
    ev_to_ebitda = safe_divide(enterprise_value, fundamental_data.ebitda)

    # Profitability metrics
    net_margin = safe_divide(fundamental_data.net_income, fundamental_data.revenue)
    ebitda_margin = safe_divide(fundamental_data.ebitda, fundamental_data.revenue)
    roe = safe_divide(fundamental_data.net_income, fundamental_data.total_equity)

    # Growth metrics
    revenue_growth = fundamental_data.revenue_growth

    # Leverage metrics
    debt_to_equity = safe_divide(fundamental_data.total_debt, fundamental_data.total_equity)
    debt_to_assets = safe_divide(fundamental_data.total_debt, fundamental_data.total_assets)
    net_debt = fundamental_data.total_debt - fundamental_data.cash
    net_debt_to_ebitda = safe_divide(net_debt, fundamental_data.ebitda)

    # Quality metrics
    fcf_margin = safe_divide(fundamental_data.free_cash_flow, fundamental_data.revenue)
    # Mock current ratio (current assets / current liabilities)
    # In real implementation, would need actual current assets/liabilities
    current_ratio = safe_divide(fundamental_data.cash, fundamental_data.total_debt * 0.3)

    # Market metrics
    beta = market_data.beta
    market_cap = market_data.market_cap
    distance_from_52w_high = safe_divide(
        market_data.price_52w_high - market_data.price,
        market_data.price
    )

    return RawMetrics(
        ticker=ticker,
        price_to_sales=price_to_sales,
        price_to_book=price_to_book,
        ev_to_ebitda=ev_to_ebitda,
        net_margin=net_margin,
        ebitda_margin=ebitda_margin,
        roe=roe,
        revenue_growth=revenue_growth,
        debt_to_equity=debt_to_equity,
        debt_to_assets=debt_to_assets,
        net_debt_to_ebitda=net_debt_to_ebitda,
        fcf_margin=fcf_margin,
        current_ratio=current_ratio,
        beta=beta,
        market_cap=market_cap,
        distance_from_52w_high=distance_from_52w_high,
        sector=fundamental_data.sector,
        industry=fundamental_data.industry
    )


def percentile_rank(value: float, values: List[float], reverse: bool = False) -> float:
    """
    Compute percentile rank of a value within a list of values.

    Args:
        value: The value to rank
        values: List of all values
        reverse: If True, lower values get higher percentiles (for bearish scoring)
                 e.g., for profitability, low margin = high score (more bearish)

    Returns:
        Percentile rank (0-100)
    """
    if not values:
        return 50.0

    sorted_values = sorted(values)

    # Find position of value
    count_below = sum(1 for v in sorted_values if v < value)
    count_equal = sum(1 for v in sorted_values if v == value)

    # Calculate percentile using midpoint method
    percentile = 100.0 * (count_below + count_equal / 2.0) / len(values)

    # If reverse, invert the percentile
    # Low values get high percentiles (bearish)
    if reverse:
        percentile = 100.0 - percentile

    return min(max(percentile, 0.0), 100.0)


def compute_factor_scores(
    raw_metrics: RawMetrics,
    universe_metrics: List[RawMetrics]
) -> FactorScores:
    """
    Compute percentile-based factor scores for a ticker.

    Higher scores indicate more bearish characteristics.

    Args:
        raw_metrics: Raw metrics for the ticker
        universe_metrics: Raw metrics for all tickers in the universe

    Returns:
        FactorScores object with percentile-based scores
    """
    # Extract metric values from universe
    def extract_values(attr: str) -> List[float]:
        return [getattr(m, attr) for m in universe_metrics]

    # Valuation score (higher valuation = more bearish)
    ps_percentile = percentile_rank(
        raw_metrics.price_to_sales,
        extract_values('price_to_sales')
    )
    pb_percentile = percentile_rank(
        raw_metrics.price_to_book,
        extract_values('price_to_book')
    )
    ev_ebitda_percentile = percentile_rank(
        raw_metrics.ev_to_ebitda,
        extract_values('ev_to_ebitda')
    )
    valuation_score = statistics.mean([ps_percentile, pb_percentile, ev_ebitda_percentile])

    # Profitability score (lower profitability = more bearish)
    # Reverse percentile so low profitability gets high score
    net_margin_percentile = percentile_rank(
        raw_metrics.net_margin,
        extract_values('net_margin'),
        reverse=True
    )
    ebitda_margin_percentile = percentile_rank(
        raw_metrics.ebitda_margin,
        extract_values('ebitda_margin'),
        reverse=True
    )
    roe_percentile = percentile_rank(
        raw_metrics.roe,
        extract_values('roe'),
        reverse=True
    )
    profitability_score = statistics.mean([
        net_margin_percentile,
        ebitda_margin_percentile,
        roe_percentile
    ])

    # Growth score (negative/low growth = more bearish)
    growth_score = percentile_rank(
        raw_metrics.revenue_growth,
        extract_values('revenue_growth'),
        reverse=True
    )

    # Leverage score (higher leverage = more bearish)
    de_percentile = percentile_rank(
        raw_metrics.debt_to_equity,
        extract_values('debt_to_equity')
    )
    da_percentile = percentile_rank(
        raw_metrics.debt_to_assets,
        extract_values('debt_to_assets')
    )
    nd_ebitda_percentile = percentile_rank(
        raw_metrics.net_debt_to_ebitda,
        extract_values('net_debt_to_ebitda')
    )
    leverage_score = statistics.mean([de_percentile, da_percentile, nd_ebitda_percentile])

    # Quality score (lower quality = more bearish)
    fcf_margin_percentile = percentile_rank(
        raw_metrics.fcf_margin,
        extract_values('fcf_margin'),
        reverse=True
    )
    current_ratio_percentile = percentile_rank(
        raw_metrics.current_ratio,
        extract_values('current_ratio'),
        reverse=True
    )
    quality_score = statistics.mean([fcf_margin_percentile, current_ratio_percentile])

    # Market score (higher beta and distance from high = more bearish)
    beta_percentile = percentile_rank(
        raw_metrics.beta,
        extract_values('beta')
    )
    distance_percentile = percentile_rank(
        raw_metrics.distance_from_52w_high,
        extract_values('distance_from_52w_high')
    )
    market_score = statistics.mean([beta_percentile, distance_percentile])

    return FactorScores(
        ticker=raw_metrics.ticker,
        valuation_score=valuation_score,
        profitability_score=profitability_score,
        growth_score=growth_score,
        leverage_score=leverage_score,
        quality_score=quality_score,
        market_score=market_score
    )


def compute_all_factor_scores(
    universe_metrics: List[RawMetrics]
) -> Dict[str, FactorScores]:
    """
    Compute factor scores for all tickers in the universe.

    Args:
        universe_metrics: List of raw metrics for all tickers

    Returns:
        Dictionary mapping tickers to their factor scores
    """
    return {
        metrics.ticker: compute_factor_scores(metrics, universe_metrics)
        for metrics in universe_metrics
    }
