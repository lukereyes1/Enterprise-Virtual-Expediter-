"""
Screening models for short candidates.

Models representing the output of the screening engine.
"""

from typing import Dict
from pydantic import BaseModel, Field


class ShortCandidate(BaseModel):
    """
    A short candidate with all relevant scores and metadata.
    """
    ticker: str = Field(description="Stock ticker symbol")
    global_vulnerability_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Overall vulnerability score (0-100)"
    )
    dominant_theme: str = Field(description="Theme with highest score")
    dominant_theme_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Score for dominant theme"
    )

    # Individual theme scores
    theme_scores: Dict[str, float] = Field(
        description="Scores for all themes"
    )

    # Factor scores
    valuation_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Valuation factor score"
    )
    profitability_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Profitability factor score"
    )
    growth_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Growth factor score"
    )
    leverage_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Leverage factor score"
    )
    quality_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Quality factor score"
    )
    market_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Market factor score"
    )

    # Key raw metrics
    market_cap: float = Field(description="Market cap in millions")
    sector: str = Field(description="Sector classification")
    revenue_growth: float = Field(description="Revenue growth rate")
    net_margin: float = Field(description="Net profit margin")
    debt_to_equity: float = Field(description="Debt-to-Equity ratio")
    beta: float = Field(description="Market beta")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "TSLA",
                    "global_vulnerability_score": 78.4,
                    "dominant_theme": "Unprofitable Growth",
                    "dominant_theme_score": 82.1,
                    "theme_scores": {
                        "Unprofitable Growth": 82.1,
                        "Over-Leveraged Small Caps": 65.3,
                        "High Beta Consumer": 75.8,
                        "Weak Financials": 68.9
                    },
                    "valuation_score": 85.3,
                    "profitability_score": 72.4,
                    "growth_score": 45.6,
                    "leverage_score": 67.8,
                    "quality_score": 63.1,
                    "market_score": 88.9,
                    "market_cap": 800000.0,
                    "sector": "Consumer Discretionary",
                    "revenue_growth": 0.51,
                    "net_margin": 0.03,
                    "debt_to_equity": 0.87,
                    "beta": 2.01
                }
            ]
        }
    }
