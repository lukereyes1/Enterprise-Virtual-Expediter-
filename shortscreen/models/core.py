"""
Core domain models for ShortScreen.

Includes MacroRegime, FactorScores, RawMetrics, and ThemeConfig.
"""

from typing import Dict
from pydantic import BaseModel, Field, field_validator


class MacroRegime(BaseModel):
    """
    Macro regime indicators.

    Each indicator is a value between 0 and 1, where higher values
    indicate stronger conditions for that regime.
    """
    downturn: float = Field(
        ge=0.0,
        le=1.0,
        description="Economic downturn risk (0-1)"
    )
    inflation: float = Field(
        ge=0.0,
        le=1.0,
        description="Inflation pressure (0-1)"
    )
    liquidity: float = Field(
        ge=0.0,
        le=1.0,
        description="Liquidity stress (0-1)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "downturn": 0.8,
                    "inflation": 0.6,
                    "liquidity": 0.7
                }
            ]
        }
    }


class ThemeConfig(BaseModel):
    """Configuration for a single theme."""
    base_weight: float = Field(
        gt=0.0,
        description="Baseline weight for the theme"
    )
    sensitivities: Dict[str, float] = Field(
        description="Sensitivities to macro factors (downturn, inflation, liquidity)"
    )

    @field_validator('sensitivities')
    @classmethod
    def validate_sensitivities(cls, v: Dict[str, float]) -> Dict[str, float]:
        """Validate that all required sensitivities are present."""
        required_keys = {'downturn', 'inflation', 'liquidity'}
        if not required_keys.issubset(v.keys()):
            raise ValueError(f"Sensitivities must include: {required_keys}")
        return v


class RawMetrics(BaseModel):
    """
    Raw financial and market metrics for a ticker.

    These metrics are computed from market and fundamental data and serve
    as inputs to factor score calculations.
    """
    ticker: str = Field(description="Stock ticker symbol")

    # Valuation metrics
    price_to_sales: float = Field(description="Price-to-Sales ratio")
    price_to_book: float = Field(description="Price-to-Book ratio")
    ev_to_ebitda: float = Field(description="EV/EBITDA ratio")

    # Profitability metrics
    net_margin: float = Field(description="Net profit margin")
    ebitda_margin: float = Field(description="EBITDA margin")
    roe: float = Field(description="Return on Equity")

    # Growth metrics
    revenue_growth: float = Field(description="Year-over-year revenue growth rate")

    # Leverage metrics
    debt_to_equity: float = Field(description="Debt-to-Equity ratio")
    debt_to_assets: float = Field(description="Debt-to-Assets ratio")
    net_debt_to_ebitda: float = Field(description="Net Debt to EBITDA ratio")

    # Quality metrics
    fcf_margin: float = Field(description="Free Cash Flow margin")
    current_ratio: float = Field(description="Current ratio (liquidity)")

    # Market metrics
    beta: float = Field(description="Market beta")
    market_cap: float = Field(description="Market capitalization in millions")
    distance_from_52w_high: float = Field(
        description="Distance from 52-week high as percentage"
    )

    # Sector/Industry
    sector: str = Field(description="Sector classification")
    industry: str = Field(description="Industry classification")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "AAPL",
                    "price_to_sales": 7.5,
                    "price_to_book": 45.2,
                    "ev_to_ebitda": 24.3,
                    "net_margin": 0.25,
                    "ebitda_margin": 0.30,
                    "roe": 1.47,
                    "revenue_growth": 0.08,
                    "debt_to_equity": 1.78,
                    "debt_to_assets": 0.32,
                    "net_debt_to_ebitda": 0.85,
                    "fcf_margin": 0.23,
                    "current_ratio": 0.93,
                    "beta": 1.24,
                    "market_cap": 2800000.0,
                    "distance_from_52w_high": 0.15,
                    "sector": "Technology",
                    "industry": "Consumer Electronics"
                }
            ]
        }
    }


class FactorScores(BaseModel):
    """
    Percentile-based factor scores for a ticker.

    Each score is a percentile rank (0-100) where higher values indicate
    more bearish characteristics for that factor.
    """
    ticker: str = Field(description="Stock ticker symbol")

    valuation_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Valuation score (higher = more expensive = more bearish)"
    )
    profitability_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Profitability score (higher = less profitable = more bearish)"
    )
    growth_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Growth score (higher = negative/slowing growth = more bearish)"
    )
    leverage_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Leverage score (higher = more levered = more bearish)"
    )
    quality_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Quality score (higher = lower quality = more bearish)"
    )
    market_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Market score (higher = higher beta/momentum issues = more bearish)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "AAPL",
                    "valuation_score": 85.3,
                    "profitability_score": 12.4,
                    "growth_score": 45.6,
                    "leverage_score": 67.8,
                    "quality_score": 23.1,
                    "market_score": 78.9
                }
            ]
        }
    }
