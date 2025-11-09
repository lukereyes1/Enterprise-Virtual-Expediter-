"""
Chart generation for screening reports.

This module provides functionality to generate charts and visualizations
for screening reports using matplotlib.
"""

from pathlib import Path
from typing import List, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from shortscreen.models.reports import (
    ScreeningReport,
    SectorDistribution,
    ThemeDistribution,
    FactorDistribution,
)


class ChartGenerator:
    """
    Generate charts for screening reports.

    Provides methods to create various visualizations of screening results.
    """

    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """
        Initialize chart generator.

        Args:
            style: Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except:
            # Fallback to default if style not available
            pass

    def generate_all_charts(
        self,
        report: ScreeningReport,
        output_dir: Path
    ) -> List[Path]:
        """
        Generate all charts for a report.

        Args:
            report: Screening report
            output_dir: Directory to save charts

        Returns:
            List of paths to generated chart files
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        chart_paths = []

        # Sector distribution chart
        sector_chart = self.generate_sector_chart(
            report.sector_distribution,
            output_dir / "sector_distribution.png"
        )
        if sector_chart:
            chart_paths.append(sector_chart)

        # Theme distribution chart
        theme_chart = self.generate_theme_chart(
            report.theme_distribution,
            output_dir / "theme_distribution.png"
        )
        if theme_chart:
            chart_paths.append(theme_chart)

        # Factor distributions chart
        factor_chart = self.generate_factor_distributions_chart(
            report.factor_distributions,
            output_dir / "factor_distributions.png"
        )
        if factor_chart:
            chart_paths.append(factor_chart)

        # Risk indicators chart
        risk_chart = self.generate_risk_indicators_chart(
            report.risk_indicators,
            output_dir / "risk_indicators.png"
        )
        if risk_chart:
            chart_paths.append(risk_chart)

        return chart_paths

    def generate_sector_chart(
        self,
        sector_dist: List[SectorDistribution],
        output_path: Path
    ) -> Optional[Path]:
        """Generate sector distribution pie chart."""
        if not sector_dist:
            return None

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Pie chart of counts
        sectors = [s.sector for s in sector_dist]
        counts = [s.count for s in sector_dist]
        colors = plt.cm.Set3(range(len(sectors)))

        ax1.pie(counts, labels=sectors, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('Sector Distribution (by count)', fontsize=14, fontweight='bold')

        # Bar chart of average scores
        avg_scores = [s.avg_score for s in sector_dist]
        bars = ax2.barh(range(len(sectors)), avg_scores, color=colors)
        ax2.set_yticks(range(len(sectors)))
        ax2.set_yticklabels(sectors)
        ax2.set_xlabel('Average Vulnerability Score', fontsize=11)
        ax2.set_title('Average Score by Sector', fontsize=14, fontweight='bold')
        ax2.set_xlim(0, 100)

        # Add value labels on bars
        for i, (bar, score) in enumerate(zip(bars, avg_scores)):
            ax2.text(score + 1, i, f'{score:.1f}', va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def generate_theme_chart(
        self,
        theme_dist: List[ThemeDistribution],
        output_path: Path
    ) -> Optional[Path]:
        """Generate theme distribution chart."""
        if not theme_dist:
            return None

        fig, ax = plt.subplots(figsize=(10, 6))

        themes = [t.theme for t in theme_dist]
        percentages = [t.percentage for t in theme_dist]
        avg_scores = [t.avg_score for t in theme_dist]

        # Create bar chart with dual y-axes
        x = range(len(themes))
        width = 0.35

        # Percentage bars
        ax.bar([i - width/2 for i in x], percentages, width,
               label='% of Candidates', color='steelblue', alpha=0.7)

        # Average score bars
        ax.bar([i + width/2 for i in x], avg_scores, width,
               label='Avg Score', color='coral', alpha=0.7)

        ax.set_ylabel('Value', fontsize=11)
        ax.set_title('Theme Distribution and Scores', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(themes, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def generate_factor_distributions_chart(
        self,
        factor_dists: List[FactorDistribution],
        output_path: Path
    ) -> Optional[Path]:
        """Generate factor distributions box plot."""
        if not factor_dists:
            return None

        fig, ax = plt.subplots(figsize=(12, 6))

        factors = [f.factor.capitalize() for f in factor_dists]
        positions = range(1, len(factors) + 1)

        # Create box plot data
        box_data = []
        for f in factor_dists:
            # Reconstruct approximate distribution from statistics
            # Note: This is an approximation for visualization
            box_data.append([f.min, f.p25, f.median, f.p75, f.max])

        bp = ax.boxplot(
            [[d[0], d[1], d[2], d[3], d[4]] for d in box_data],
            positions=positions,
            widths=0.6,
            patch_artist=True,
            showmeans=True,
            meanprops=dict(marker='D', markerfacecolor='red', markersize=6)
        )

        # Color the boxes
        colors = plt.cm.Set2(range(len(factors)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_xticklabels(factors)
        ax.set_ylabel('Score (0-100)', fontsize=11)
        ax.set_title('Factor Score Distributions', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, 100)

        # Add legend
        mean_patch = mpatches.Patch(color='red', label='Mean')
        ax.legend(handles=[mean_patch], loc='upper right')

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def generate_risk_indicators_chart(
        self,
        risk_indicators,
        output_path: Path
    ) -> Optional[Path]:
        """Generate risk indicators gauge chart."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()

        indicators = [
            ('Risk-Off Score', risk_indicators.risk_off_score),
            ('Small Cap Stress', risk_indicators.small_cap_stress_score),
            ('Leverage Stress', risk_indicators.leverage_stress_score),
            ('Valuation Extremes', risk_indicators.valuation_extremes_score),
        ]

        for ax, (name, value) in zip(axes, indicators):
            self._draw_gauge(ax, name, value)

        plt.suptitle('Risk Indicators', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def _draw_gauge(self, ax, name: str, value: float):
        """Draw a single gauge indicator."""
        # Determine color based on value
        if value < 40:
            color = 'green'
            level = 'Low'
        elif value < 70:
            color = 'orange'
            level = 'Moderate'
        else:
            color = 'red'
            level = 'High'

        # Draw gauge arc
        theta = (value / 100) * 180  # 0-180 degrees
        ax.barh(0, value, height=0.3, color=color, alpha=0.7)
        ax.barh(0, 100 - value, left=value, height=0.3, color='lightgray', alpha=0.3)

        # Add text
        ax.text(50, 0, f'{value:.1f}', ha='center', va='center',
                fontsize=24, fontweight='bold')
        ax.text(50, -0.5, level, ha='center', va='top',
                fontsize=12, color=color, fontweight='bold')

        ax.set_xlim(0, 100)
        ax.set_ylim(-1, 0.5)
        ax.axis('off')
        ax.set_title(name, fontsize=12, fontweight='bold', pad=10)
