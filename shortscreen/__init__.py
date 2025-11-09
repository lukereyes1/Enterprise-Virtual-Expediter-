"""
ShortScreen: A macro-to-theme-to-target engine for bearish investment ideas.

This package implements a systematic framework for identifying short candidates
based on macro regimes, thematic vulnerabilities, and fundamental factors.
"""

__version__ = "0.1.0"

from shortscreen.data import DataProvider
from shortscreen.factors import RawMetrics, FactorScores
from shortscreen.engine import ShortCandidate, ShortScreenEngine

__all__ = [
    "DataProvider",
    "RawMetrics",
    "FactorScores",
    "ShortCandidate",
    "ShortScreenEngine",
]
