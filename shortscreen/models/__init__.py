"""
Central models module - Single source of truth for all data models.

This module provides Pydantic models for all data structures used throughout
the ShortScreen package. These models provide:
- Runtime validation
- JSON schema generation
- Type safety
- Automatic serialization/deserialization
"""

from shortscreen.models.core import (
    MacroRegime,
    ThemeConfig,
    FactorScores,
    RawMetrics,
)
from shortscreen.models.data import (
    MarketData,
    FundamentalData,
)
from shortscreen.models.screening import (
    ShortCandidate,
)
from shortscreen.models.jobs import (
    JobType,
    JobStatus,
    JobPhaseMetrics,
    JobResult,
)

__all__ = [
    # Core models
    'MacroRegime',
    'ThemeConfig',
    'FactorScores',
    'RawMetrics',
    # Data models
    'MarketData',
    'FundamentalData',
    # Screening models
    'ShortCandidate',
    # Job models
    'JobType',
    'JobStatus',
    'JobPhaseMetrics',
    'JobResult',
]
