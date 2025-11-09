#!/usr/bin/env python
"""
Test script for comprehensive reporting system.

Demonstrates full workflow: screen → generate report → create charts → export.
"""

import time
from pathlib import Path

from shortscreen.engine import ShortScreenEngine
from shortscreen.macro import MacroRegime
from shortscreen.reporting import ReportGenerator
from shortscreen.charts import ChartGenerator
from shortscreen.export import ReportExporter


def main():
    """Run complete reporting workflow."""
    print("="*70)
    print("ShortScreen Comprehensive Reporting System Test")
    print("="*70)
    print()

    # Step 1: Run screening
    print("Step 1: Running screening engine...")
    engine = ShortScreenEngine()
    regime = MacroRegime(downturn=0.8, inflation=0.6, liquidity=0.7)

    start_time = time.time()
    candidates = engine.run(regime)
    execution_time = time.time() - start_time

    print(f"  ✓ Found {len(candidates)} candidates in {execution_time:.2f}s")
    print()

    # Step 2: Generate report
    print("Step 2: Generating comprehensive report...")
    generator = ReportGenerator()
    report = generator.generate_report(
        candidates=candidates,
        regime=regime,
        universe_size=100,
        execution_time=execution_time,
        top_n=20,
        include_narrative=True
    )

    print(f"  ✓ Report ID: {report.metadata.report_id}")
    print(f"  ✓ Risk-off score: {report.risk_indicators.risk_off_score:.1f}")
    print(f"  ✓ Top sector: {report.sector_distribution[0].sector} ({report.sector_distribution[0].percentage:.1f}%)")
    print(f"  ✓ Dominant theme: {report.theme_distribution[0].theme}")
    print()

    # Step 3: Generate charts
    print("Step 3: Generating charts...")
    chart_dir = Path("output/charts")
    chart_generator = ChartGenerator()

    try:
        chart_paths = chart_generator.generate_all_charts(report, chart_dir)
        print(f"  ✓ Generated {len(chart_paths)} charts:")
        for path in chart_paths:
            print(f"    - {path}")
    except Exception as e:
        print(f"  ⚠ Charts skipped (display not available): {e}")
        chart_paths = []

    print()

    # Step 4: Export reports
    print("Step 4: Exporting reports...")
    export_dir = Path("output/reports")
    exporter = ReportExporter()

    exports = exporter.export_all(
        report,
        export_dir,
        include_charts=bool(chart_paths)
    )

    print(f"  ✓ Exported {len(exports)} formats:")
    for format_name, path in exports.items():
        print(f"    - {format_name}: {path}")
    print()

    # Step 5: Display narrative summary
    print("Step 5: Narrative Summary")
    print("-" * 70)
    print()
    print(f"Headline: {report.narrative.headline}")
    print()
    print("Key Findings:")
    for finding in report.narrative.key_findings:
        print(f"  • {finding}")
    print()
    print("Risk Assessment:")
    print(f"  {report.narrative.risk_assessment}")
    print()
    print("Recommendations:")
    for rec in report.narrative.recommendations:
        print(f"  • {rec}")
    print()

    # Summary
    print("="*70)
    print("✓ Reporting system test complete!")
    print()
    print(f"Generated files:")
    print(f"  - Reports: {export_dir}")
    if chart_paths:
        print(f"  - Charts: {chart_dir}")
    print()


if __name__ == "__main__":
    main()
