"""
Report generation for screening results.

This module provides functionality to generate comprehensive reports from
screening results, including metadata, risk indicators, distributions,
and narrative summaries.
"""

import statistics
from datetime import datetime
from typing import List, Dict, Optional
from collections import Counter

from shortscreen.models.core import MacroRegime
from shortscreen.models.screening import ShortCandidate
from shortscreen.models.reports import (
    ReportMetadata,
    RiskIndicators,
    SectorDistribution,
    ThemeDistribution,
    FactorDistribution,
    NarrativeSummary,
    ScreeningReport,
)


class ReportGenerator:
    """
    Generate comprehensive screening reports.

    This class analyzes screening results and generates structured reports
    with metadata, risk indicators, distributions, and narratives.
    """

    def __init__(self, report_id: Optional[str] = None):
        """
        Initialize the report generator.

        Args:
            report_id: Optional report ID. If None, generates timestamp-based ID.
        """
        if report_id is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_id = f"report_{timestamp}"

        self.report_id = report_id

    def generate_report(
        self,
        candidates: List[ShortCandidate],
        regime: MacroRegime,
        universe_size: int,
        execution_time: float,
        top_n: int = 50,
        include_all: bool = False,
        include_narrative: bool = True
    ) -> ScreeningReport:
        """
        Generate a comprehensive screening report.

        Args:
            candidates: List of short candidates (sorted by score descending)
            regime: Macro regime used for screening
            universe_size: Total universe size
            execution_time: Execution time in seconds
            top_n: Number of top candidates to include
            include_all: Whether to include all candidates in JSON export
            include_narrative: Whether to generate narrative summary

        Returns:
            ScreeningReport with all components
        """
        # Generate metadata
        metadata = self._generate_metadata(
            candidates,
            regime,
            universe_size,
            execution_time
        )

        # Compute risk indicators
        risk_indicators = self._compute_risk_indicators(candidates, regime)

        # Get top N candidates
        top_candidates = candidates[:top_n]

        # Compute distributions
        sector_dist = self._compute_sector_distribution(candidates)
        theme_dist = self._compute_theme_distribution(candidates)
        factor_dist = self._compute_factor_distributions(candidates)

        # Generate narrative (if requested)
        narrative = None
        if include_narrative:
            narrative = self._generate_narrative(
                candidates,
                regime,
                risk_indicators,
                sector_dist,
                theme_dist
            )

        # Build report
        report = ScreeningReport(
            metadata=metadata,
            risk_indicators=risk_indicators,
            top_candidates=top_candidates,
            sector_distribution=sector_dist,
            theme_distribution=theme_dist,
            factor_distributions=factor_dist,
            narrative=narrative,
            all_candidates=candidates if include_all else None
        )

        return report

    def _generate_metadata(
        self,
        candidates: List[ShortCandidate],
        regime: MacroRegime,
        universe_size: int,
        execution_time: float
    ) -> ReportMetadata:
        """Generate report metadata."""
        return ReportMetadata(
            report_id=self.report_id,
            timestamp=datetime.now(),
            regime=regime,
            universe_size=universe_size,
            candidates_count=len(candidates),
            execution_time_seconds=execution_time
        )

    def _compute_risk_indicators(
        self,
        candidates: List[ShortCandidate],
        regime: MacroRegime
    ) -> RiskIndicators:
        """
        Compute risk indicator scores.

        Risk indicators provide high-level market stress assessments.
        """
        if not candidates:
            return RiskIndicators(
                risk_off_score=0.0,
                small_cap_stress_score=0.0,
                leverage_stress_score=0.0,
                valuation_extremes_score=0.0
            )

        # Risk-off score: weighted combination of regime and average vulnerability
        avg_vulnerability = statistics.mean(c.global_vulnerability_score for c in candidates[:100])
        regime_stress = (regime.downturn + regime.inflation + regime.liquidity) / 3.0 * 100
        risk_off_score = (avg_vulnerability * 0.6 + regime_stress * 0.4)

        # Small cap stress: average score of small cap candidates
        small_cap_candidates = [
            c for c in candidates
            if c.market_cap < 2000  # Under $2B market cap
        ]
        if small_cap_candidates:
            small_cap_stress = statistics.mean(
                c.global_vulnerability_score for c in small_cap_candidates[:50]
            )
        else:
            small_cap_stress = 0.0

        # Leverage stress: average leverage score across candidates
        leverage_stress = statistics.mean(c.leverage_score for c in candidates[:100])

        # Valuation extremes: percentage of candidates with extreme valuations
        extreme_valuations = sum(
            1 for c in candidates[:100] if c.valuation_score > 80
        )
        valuation_extremes = (extreme_valuations / min(100, len(candidates))) * 100

        return RiskIndicators(
            risk_off_score=risk_off_score,
            small_cap_stress_score=small_cap_stress,
            leverage_stress_score=leverage_stress,
            valuation_extremes_score=valuation_extremes
        )

    def _compute_sector_distribution(
        self,
        candidates: List[ShortCandidate]
    ) -> List[SectorDistribution]:
        """Compute distribution of candidates by sector."""
        if not candidates:
            return []

        # Count candidates per sector
        sector_counts = Counter(c.sector for c in candidates)

        # Compute sector scores
        sector_scores = {}
        for sector in sector_counts.keys():
            sector_candidates = [c for c in candidates if c.sector == sector]
            sector_scores[sector] = statistics.mean(
                c.global_vulnerability_score for c in sector_candidates
            )

        # Build distribution
        total = len(candidates)
        distribution = [
            SectorDistribution(
                sector=sector,
                count=count,
                percentage=(count / total * 100),
                avg_score=sector_scores[sector]
            )
            for sector, count in sector_counts.most_common()
        ]

        return distribution

    def _compute_theme_distribution(
        self,
        candidates: List[ShortCandidate]
    ) -> List[ThemeDistribution]:
        """Compute distribution of candidates by dominant theme."""
        if not candidates:
            return []

        # Count candidates per theme
        theme_counts = Counter(c.dominant_theme for c in candidates)

        # Compute theme scores
        theme_scores = {}
        for theme in theme_counts.keys():
            theme_candidates = [c for c in candidates if c.dominant_theme == theme]
            theme_scores[theme] = statistics.mean(
                c.dominant_theme_score for c in theme_candidates
            )

        # Build distribution
        total = len(candidates)
        distribution = [
            ThemeDistribution(
                theme=theme,
                count=count,
                percentage=(count / total * 100),
                avg_score=theme_scores[theme]
            )
            for theme, count in theme_counts.most_common()
        ]

        return distribution

    def _compute_factor_distributions(
        self,
        candidates: List[ShortCandidate]
    ) -> List[FactorDistribution]:
        """Compute statistical distributions of factor scores."""
        if not candidates:
            return []

        factors = [
            ('valuation', [c.valuation_score for c in candidates]),
            ('profitability', [c.profitability_score for c in candidates]),
            ('growth', [c.growth_score for c in candidates]),
            ('leverage', [c.leverage_score for c in candidates]),
            ('quality', [c.quality_score for c in candidates]),
            ('market', [c.market_score for c in candidates]),
        ]

        distributions = []
        for factor_name, scores in factors:
            if scores:
                sorted_scores = sorted(scores)
                n = len(sorted_scores)

                distributions.append(
                    FactorDistribution(
                        factor=factor_name,
                        mean=statistics.mean(scores),
                        median=statistics.median(scores),
                        std=statistics.stdev(scores) if n > 1 else 0.0,
                        min=min(scores),
                        max=max(scores),
                        p25=sorted_scores[n // 4],
                        p75=sorted_scores[3 * n // 4]
                    )
                )

        return distributions

    def _generate_narrative(
        self,
        candidates: List[ShortCandidate],
        regime: MacroRegime,
        risk_indicators: RiskIndicators,
        sector_dist: List[SectorDistribution],
        theme_dist: List[ThemeDistribution]
    ) -> NarrativeSummary:
        """
        Generate narrative summary using rules-based logic.

        This provides human-readable interpretation of the results.
        """
        # Generate headline
        headline = self._generate_headline(
            len(candidates),
            risk_indicators,
            theme_dist
        )

        # Generate key findings
        key_findings = self._generate_key_findings(
            candidates,
            regime,
            risk_indicators,
            sector_dist,
            theme_dist
        )

        # Generate risk assessment
        risk_assessment = self._generate_risk_assessment(
            risk_indicators,
            regime
        )

        # Generate sector insights
        sector_insights = self._generate_sector_insights(sector_dist)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_indicators,
            regime,
            theme_dist
        )

        return NarrativeSummary(
            headline=headline,
            key_findings=key_findings,
            risk_assessment=risk_assessment,
            sector_insights=sector_insights,
            recommendations=recommendations
        )

    def _generate_headline(
        self,
        candidate_count: int,
        risk_indicators: RiskIndicators,
        theme_dist: List[ThemeDistribution]
    ) -> str:
        """Generate headline summary."""
        if not theme_dist:
            return f"{candidate_count} vulnerable candidates identified"

        dominant_theme = theme_dist[0].theme
        risk_level = "elevated" if risk_indicators.risk_off_score > 60 else "moderate"

        return f"{risk_level.capitalize()} stress with {candidate_count} vulnerable candidates dominated by {dominant_theme}"

    def _generate_key_findings(
        self,
        candidates: List[ShortCandidate],
        regime: MacroRegime,
        risk_indicators: RiskIndicators,
        sector_dist: List[SectorDistribution],
        theme_dist: List[ThemeDistribution]
    ) -> List[str]:
        """Generate bullet points of key findings."""
        findings = []

        # Candidate count
        findings.append(f"{len(candidates)} vulnerable candidates identified")

        # Sector concentration
        if sector_dist:
            top_sector = sector_dist[0]
            findings.append(
                f"{top_sector.sector} represents {top_sector.percentage:.1f}% of vulnerable names"
            )

        # Risk indicators
        if risk_indicators.risk_off_score > 70:
            findings.append(f"Risk-off score at {risk_indicators.risk_off_score:.1f} (high)")
        elif risk_indicators.risk_off_score > 50:
            findings.append(f"Risk-off score at {risk_indicators.risk_off_score:.1f} (moderate)")

        if risk_indicators.small_cap_stress_score > 60:
            findings.append(
                f"Small cap stress score at {risk_indicators.small_cap_stress_score:.1f} (elevated)"
            )

        # Theme distribution
        if theme_dist:
            top_theme = theme_dist[0]
            findings.append(
                f"{top_theme.theme} is dominant theme for {top_theme.percentage:.1f}% of candidates"
            )

        return findings

    def _generate_risk_assessment(
        self,
        risk_indicators: RiskIndicators,
        regime: MacroRegime
    ) -> str:
        """Generate overall risk assessment paragraph."""
        risk_level = "elevated" if risk_indicators.risk_off_score > 60 else "moderate"

        assessment = f"Market conditions show {risk_level} vulnerability "

        # Add regime context
        regime_factors = []
        if regime.downturn > 0.6:
            regime_factors.append("downturn risk")
        if regime.inflation > 0.6:
            regime_factors.append("inflation pressure")
        if regime.liquidity > 0.6:
            regime_factors.append("liquidity stress")

        if regime_factors:
            assessment += f"driven by {', '.join(regime_factors)}. "
        else:
            assessment += "under current macro conditions. "

        # Add specific risk insights
        if risk_indicators.leverage_stress_score > 70:
            assessment += "Leverage stress is particularly elevated. "

        if risk_indicators.valuation_extremes_score > 60:
            assessment += "A significant portion of candidates show extreme valuations. "

        return assessment

    def _generate_sector_insights(
        self,
        sector_dist: List[SectorDistribution]
    ) -> str:
        """Generate sector-specific insights."""
        if not sector_dist:
            return "No sector-specific patterns identified."

        insights = []

        # Top sector
        top_sector = sector_dist[0]
        insights.append(
            f"{top_sector.sector} is heavily represented with {top_sector.count} candidates "
            f"({top_sector.percentage:.1f}%) averaging {top_sector.avg_score:.1f} vulnerability score."
        )

        # Additional sectors
        if len(sector_dist) > 1:
            other_sectors = ", ".join(s.sector for s in sector_dist[1:3])
            insights.append(
                f"Other concentrated sectors include {other_sectors}."
            )

        return " ".join(insights)

    def _generate_recommendations(
        self,
        risk_indicators: RiskIndicators,
        regime: MacroRegime,
        theme_dist: List[ThemeDistribution]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Based on risk level
        if risk_indicators.risk_off_score > 70:
            recommendations.append("Consider increasing hedges given elevated risk-off environment")

        # Based on specific risks
        if risk_indicators.small_cap_stress_score > 65:
            recommendations.append("Monitor leveraged small caps closely for potential distress")

        if risk_indicators.leverage_stress_score > 75:
            recommendations.append("Review exposure to highly leveraged names")

        # Based on dominant theme
        if theme_dist:
            top_theme = theme_dist[0].theme
            if "Consumer" in top_theme and regime.downturn > 0.6:
                recommendations.append("Consider hedging high-beta consumer exposure")
            elif "Leverage" in top_theme and regime.liquidity > 0.6:
                recommendations.append("Focus on companies with upcoming debt maturities")

        # Default recommendation
        if not recommendations:
            recommendations.append("Continue monitoring market conditions for changes in stress levels")

        return recommendations
