"""
Report export functionality.

This module provides functionality to export screening reports in various
formats (Markdown, JSON, CSV).
"""

import json
import csv
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from shortscreen.models.reports import ScreeningReport
from shortscreen.models.screening import ShortCandidate


class ReportExporter:
    """
    Export screening reports in multiple formats.

    Provides methods to export reports as Markdown, JSON, and CSV files.
    """

    def export_all(
        self,
        report: ScreeningReport,
        output_dir: Path,
        include_charts: bool = True
    ) -> dict:
        """
        Export report in all formats.

        Args:
            report: Screening report to export
            output_dir: Directory to write export files
            include_charts: Whether to reference chart files in markdown

        Returns:
            Dictionary mapping format to file path
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        base_name = report.metadata.report_id

        exports = {}

        # Markdown
        md_path = self.export_markdown(
            report,
            output_dir / f"{base_name}.md",
            include_charts=include_charts
        )
        exports['markdown'] = md_path

        # JSON
        json_path = self.export_json(
            report,
            output_dir / f"{base_name}.json"
        )
        exports['json'] = json_path

        # CSV (top candidates)
        csv_path = self.export_candidates_csv(
            report.top_candidates,
            output_dir / f"{base_name}_top_candidates.csv"
        )
        exports['csv'] = csv_path

        return exports

    def export_markdown(
        self,
        report: ScreeningReport,
        output_path: Path,
        include_charts: bool = True
    ) -> Path:
        """
        Export report as Markdown.

        Args:
            report: Screening report
            output_path: Path to write markdown file
            include_charts: Whether to include chart references

        Returns:
            Path to exported file
        """
        lines = []

        # Title
        lines.append(f"# Screening Report: {report.metadata.report_id}")
        lines.append("")

        # Metadata
        lines.append("## Report Metadata")
        lines.append("")
        lines.append(f"- **Generated**: {report.metadata.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"- **Universe Size**: {report.metadata.universe_size:,}")
        lines.append(f"- **Candidates Found**: {report.metadata.candidates_count:,}")
        lines.append(f"- **Execution Time**: {report.metadata.execution_time_seconds:.2f}s")
        lines.append("")

        # Macro Regime
        lines.append("## Macro Regime")
        lines.append("")
        lines.append(f"- **Downturn**: {report.metadata.regime.downturn:.2f}")
        lines.append(f"- **Inflation**: {report.metadata.regime.inflation:.2f}")
        lines.append(f"- **Liquidity**: {report.metadata.regime.liquidity:.2f}")
        lines.append("")

        # Risk Indicators
        lines.append("## Risk Indicators")
        lines.append("")
        if include_charts:
            lines.append("![Risk Indicators](risk_indicators.png)")
            lines.append("")

        lines.append(f"- **Risk-Off Score**: {report.risk_indicators.risk_off_score:.1f}/100")
        lines.append(f"- **Small Cap Stress**: {report.risk_indicators.small_cap_stress_score:.1f}/100")
        lines.append(f"- **Leverage Stress**: {report.risk_indicators.leverage_stress_score:.1f}/100")
        lines.append(f"- **Valuation Extremes**: {report.risk_indicators.valuation_extremes_score:.1f}/100")
        lines.append("")

        # Narrative Summary
        if report.narrative:
            lines.append("## Executive Summary")
            lines.append("")
            lines.append(f"**{report.narrative.headline}**")
            lines.append("")

            lines.append("### Key Findings")
            lines.append("")
            for finding in report.narrative.key_findings:
                lines.append(f"- {finding}")
            lines.append("")

            lines.append("### Risk Assessment")
            lines.append("")
            lines.append(report.narrative.risk_assessment)
            lines.append("")

            lines.append("### Sector Insights")
            lines.append("")
            lines.append(report.narrative.sector_insights)
            lines.append("")

            lines.append("### Recommendations")
            lines.append("")
            for rec in report.narrative.recommendations:
                lines.append(f"- {rec}")
            lines.append("")

        # Sector Distribution
        lines.append("## Sector Distribution")
        lines.append("")
        if include_charts:
            lines.append("![Sector Distribution](sector_distribution.png)")
            lines.append("")

        lines.append("| Sector | Count | Percentage | Avg Score |")
        lines.append("|--------|-------|------------|-----------|")
        for sector in report.sector_distribution:
            lines.append(
                f"| {sector.sector} | {sector.count} | "
                f"{sector.percentage:.1f}% | {sector.avg_score:.1f} |"
            )
        lines.append("")

        # Theme Distribution
        lines.append("## Theme Distribution")
        lines.append("")
        if include_charts:
            lines.append("![Theme Distribution](theme_distribution.png)")
            lines.append("")

        lines.append("| Theme | Count | Percentage | Avg Score |")
        lines.append("|-------|-------|------------|-----------|")
        for theme in report.theme_distribution:
            lines.append(
                f"| {theme.theme} | {theme.count} | "
                f"{theme.percentage:.1f}% | {theme.avg_score:.1f} |"
            )
        lines.append("")

        # Factor Distributions
        lines.append("## Factor Score Distributions")
        lines.append("")
        if include_charts:
            lines.append("![Factor Distributions](factor_distributions.png)")
            lines.append("")

        lines.append("| Factor | Mean | Median | Std | Min | Max | P25 | P75 |")
        lines.append("|--------|------|--------|-----|-----|-----|-----|-----|")
        for factor in report.factor_distributions:
            lines.append(
                f"| {factor.factor.capitalize()} | {factor.mean:.1f} | "
                f"{factor.median:.1f} | {factor.std:.1f} | {factor.min:.1f} | "
                f"{factor.max:.1f} | {factor.p25:.1f} | {factor.p75:.1f} |"
            )
        lines.append("")

        # Top Candidates
        lines.append("## Top Candidates")
        lines.append("")
        lines.append("| Rank | Ticker | Score | Theme | Sector | Market Cap |")
        lines.append("|------|--------|-------|-------|--------|------------|")
        for i, candidate in enumerate(report.top_candidates, 1):
            lines.append(
                f"| {i} | {candidate.ticker} | {candidate.global_vulnerability_score:.1f} | "
                f"{candidate.dominant_theme} | {candidate.sector} | "
                f"${candidate.market_cap:.0f}M |"
            )
        lines.append("")

        # Write file
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))

        return output_path

    def export_json(
        self,
        report: ScreeningReport,
        output_path: Path
    ) -> Path:
        """
        Export report as JSON.

        Args:
            report: Screening report
            output_path: Path to write JSON file

        Returns:
            Path to exported file
        """
        # Convert to dict using Pydantic's model_dump
        report_dict = report.model_dump(mode='json')

        # Write JSON
        with open(output_path, 'w') as f:
            json.dump(report_dict, f, indent=2, default=str)

        return output_path

    def export_candidates_csv(
        self,
        candidates: List[ShortCandidate],
        output_path: Path
    ) -> Path:
        """
        Export candidates as CSV.

        Args:
            candidates: List of short candidates
            output_path: Path to write CSV file

        Returns:
            Path to exported file
        """
        if not candidates:
            # Write empty CSV with headers
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Ticker', 'Global Score', 'Dominant Theme', 'Theme Score',
                    'Valuation', 'Profitability', 'Growth', 'Leverage', 'Quality', 'Market',
                    'Sector', 'Market Cap', 'Revenue Growth', 'Net Margin', 'D/E', 'Beta'
                ])
            return output_path

        # Write candidates
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'Ticker', 'Global Score', 'Dominant Theme', 'Theme Score',
                'Valuation', 'Profitability', 'Growth', 'Leverage', 'Quality', 'Market',
                'Sector', 'Market Cap', 'Revenue Growth', 'Net Margin', 'D/E', 'Beta'
            ])

            # Rows
            for candidate in candidates:
                writer.writerow([
                    candidate.ticker,
                    f"{candidate.global_vulnerability_score:.2f}",
                    candidate.dominant_theme,
                    f"{candidate.dominant_theme_score:.2f}",
                    f"{candidate.valuation_score:.2f}",
                    f"{candidate.profitability_score:.2f}",
                    f"{candidate.growth_score:.2f}",
                    f"{candidate.leverage_score:.2f}",
                    f"{candidate.quality_score:.2f}",
                    f"{candidate.market_score:.2f}",
                    candidate.sector,
                    f"{candidate.market_cap:.0f}",
                    f"{candidate.revenue_growth:.3f}",
                    f"{candidate.net_margin:.3f}",
                    f"{candidate.debt_to_equity:.3f}",
                    f"{candidate.beta:.3f}",
                ])

        return output_path
