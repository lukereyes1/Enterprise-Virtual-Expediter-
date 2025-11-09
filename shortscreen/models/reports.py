"""
Report models for screening results.

Models representing report structure, metadata, metrics, and narratives.
"""

from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

from shortscreen.models.core import MacroRegime
from shortscreen.models.screening import ShortCandidate


class ReportMetadata(BaseModel):
    """Metadata for a screening report."""
    report_id: str = Field(description="Unique report identifier")
    timestamp: datetime = Field(description="Report generation timestamp")
    regime: MacroRegime = Field(description="Macro regime used for screening")
    universe_size: int = Field(ge=0, description="Total universe size")
    candidates_count: int = Field(ge=0, description="Number of candidates generated")
    execution_time_seconds: float = Field(ge=0, description="Execution time in seconds")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "report_id": "report_20250109_093000",
                    "timestamp": "2025-01-09T09:30:00Z",
                    "regime": {
                        "downturn": 0.8,
                        "inflation": 0.6,
                        "liquidity": 0.7
                    },
                    "universe_size": 5000,
                    "candidates_count": 500,
                    "execution_time_seconds": 12.5
                }
            ]
        }
    }


class RiskIndicators(BaseModel):
    """Risk indicator scores."""
    risk_off_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Overall market risk-off sentiment (0-100)"
    )
    small_cap_stress_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Small cap stress level (0-100)"
    )
    leverage_stress_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Leverage stress across universe (0-100)"
    )
    valuation_extremes_score: float = Field(
        ge=0.0,
        le=100.0,
        description="Valuation extremes indicator (0-100)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "risk_off_score": 72.5,
                    "small_cap_stress_score": 68.3,
                    "leverage_stress_score": 81.2,
                    "valuation_extremes_score": 65.7
                }
            ]
        }
    }


class SectorDistribution(BaseModel):
    """Distribution of candidates by sector."""
    sector: str = Field(description="Sector name")
    count: int = Field(ge=0, description="Number of candidates in sector")
    percentage: float = Field(ge=0.0, le=100.0, description="Percentage of total")
    avg_score: float = Field(ge=0.0, le=100.0, description="Average vulnerability score")


class ThemeDistribution(BaseModel):
    """Distribution of candidates by dominant theme."""
    theme: str = Field(description="Theme name")
    count: int = Field(ge=0, description="Number of candidates with this dominant theme")
    percentage: float = Field(ge=0.0, le=100.0, description="Percentage of total")
    avg_score: float = Field(ge=0.0, le=100.0, description="Average theme score")


class FactorDistribution(BaseModel):
    """Statistical distribution of a factor score."""
    factor: str = Field(description="Factor name")
    mean: float = Field(description="Mean score")
    median: float = Field(description="Median score")
    std: float = Field(ge=0, description="Standard deviation")
    min: float = Field(description="Minimum score")
    max: float = Field(description="Maximum score")
    p25: float = Field(description="25th percentile")
    p75: float = Field(description="75th percentile")


class NarrativeSummary(BaseModel):
    """Narrative summary of screening results."""
    headline: str = Field(description="One-line summary")
    key_findings: List[str] = Field(description="Bullet points of key findings")
    risk_assessment: str = Field(description="Overall risk assessment paragraph")
    sector_insights: str = Field(description="Sector-specific insights")
    recommendations: List[str] = Field(description="Recommended actions")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "headline": "Elevated stress in financial and consumer sectors amid high downturn risk",
                    "key_findings": [
                        "500 vulnerable candidates identified across 5000 universe",
                        "Financials represent 45% of vulnerable names",
                        "Small cap stress score at 68.3 (elevated)"
                    ],
                    "risk_assessment": "Market conditions show elevated vulnerability...",
                    "sector_insights": "Financial sector heavily represented due to...",
                    "recommendations": [
                        "Monitor leveraged small caps closely",
                        "Consider hedging high-beta consumer exposure"
                    ]
                }
            ]
        }
    }


class ScreeningReport(BaseModel):
    """Complete screening report with all components."""
    metadata: ReportMetadata = Field(description="Report metadata")
    risk_indicators: RiskIndicators = Field(description="Risk indicator scores")
    top_candidates: List[ShortCandidate] = Field(description="Top N candidates")

    # Distributions
    sector_distribution: List[SectorDistribution] = Field(
        description="Candidate distribution by sector"
    )
    theme_distribution: List[ThemeDistribution] = Field(
        description="Candidate distribution by dominant theme"
    )
    factor_distributions: List[FactorDistribution] = Field(
        description="Statistical distributions of factor scores"
    )

    # Narrative
    narrative: Optional[NarrativeSummary] = Field(
        default=None,
        description="Narrative summary (optional)"
    )

    # Raw data (for JSON export)
    all_candidates: Optional[List[ShortCandidate]] = Field(
        default=None,
        description="All candidates (optional, for full data export)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "metadata": {
                        "report_id": "report_20250109_093000",
                        "timestamp": "2025-01-09T09:30:00Z",
                        "regime": {"downturn": 0.8, "inflation": 0.6, "liquidity": 0.7},
                        "universe_size": 5000,
                        "candidates_count": 500,
                        "execution_time_seconds": 12.5
                    },
                    "risk_indicators": {
                        "risk_off_score": 72.5,
                        "small_cap_stress_score": 68.3,
                        "leverage_stress_score": 81.2,
                        "valuation_extremes_score": 65.7
                    },
                    "top_candidates": [],
                    "sector_distribution": [],
                    "theme_distribution": [],
                    "factor_distributions": []
                }
            ]
        }
    }
