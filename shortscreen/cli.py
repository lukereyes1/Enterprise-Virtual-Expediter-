"""
Command-line interface for ShortScreen.

Provides a simple CLI to run the screening engine with macro regime parameters.
"""

import argparse
import sys
from typing import List

from shortscreen.engine import ShortScreenEngine, ShortCandidate
from shortscreen.macro import MacroRegime


def format_candidate(candidate: ShortCandidate, rank: int) -> str:
    """
    Format a short candidate for display.

    Args:
        candidate: ShortCandidate object
        rank: Rank in the list (1-indexed)

    Returns:
        Formatted string
    """
    lines = [
        f"\n{'='*80}",
        f"#{rank} - {candidate.ticker} | Score: {candidate.global_vulnerability_score:.1f}",
        f"{'='*80}",
        f"Dominant Theme: {candidate.dominant_theme} (Score: {candidate.dominant_theme_score:.1f})",
        f"Sector: {candidate.sector} | Market Cap: ${candidate.market_cap:.0f}M",
        f"",
        f"Factor Scores:",
        f"  Valuation:     {candidate.valuation_score:6.1f}",
        f"  Profitability: {candidate.profitability_score:6.1f}",
        f"  Growth:        {candidate.growth_score:6.1f}",
        f"  Leverage:      {candidate.leverage_score:6.1f}",
        f"  Quality:       {candidate.quality_score:6.1f}",
        f"  Market:        {candidate.market_score:6.1f}",
        f"",
        f"Key Metrics:",
        f"  Revenue Growth: {candidate.revenue_growth*100:6.1f}%",
        f"  Net Margin:     {candidate.net_margin*100:6.1f}%",
        f"  Debt/Equity:    {candidate.debt_to_equity:6.2f}",
        f"  Beta:           {candidate.beta:6.2f}",
    ]

    return "\n".join(lines)


def print_summary(candidates: List[ShortCandidate], macro_regime: MacroRegime):
    """
    Print summary statistics.

    Args:
        candidates: List of short candidates
        macro_regime: The macro regime used
    """
    print("\n" + "="*80)
    print("SHORT SCREEN RESULTS")
    print("="*80)
    print(f"\nMacro Regime:")
    print(f"  Downturn:  {macro_regime.downturn:.2f}")
    print(f"  Inflation: {macro_regime.inflation:.2f}")
    print(f"  Liquidity: {macro_regime.liquidity:.2f}")
    print(f"\nTotal Candidates: {len(candidates)}")

    if candidates:
        avg_score = sum(c.global_vulnerability_score for c in candidates) / len(candidates)
        print(f"Average Global Score: {avg_score:.1f}")

        # Theme distribution
        theme_dist = {}
        for c in candidates[:20]:  # Top 20
            theme_dist[c.dominant_theme] = theme_dist.get(c.dominant_theme, 0) + 1

        print(f"\nTop 20 Theme Distribution:")
        for theme, count in sorted(theme_dist.items(), key=lambda x: -x[1]):
            print(f"  {theme:30s}: {count}")

        # Sector distribution
        sector_dist = {}
        for c in candidates[:20]:
            sector_dist[c.sector] = sector_dist.get(c.sector, 0) + 1

        print(f"\nTop 20 Sector Distribution:")
        for sector, count in sorted(sector_dist.items(), key=lambda x: -x[1]):
            print(f"  {sector:30s}: {count}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ShortScreen: Macro-driven short screening engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Baseline regime
  shortscreen-cli --downturn 0.5 --inflation 0.5 --liquidity 0.5

  # High stress regime
  shortscreen-cli --downturn 0.9 --inflation 0.8 --liquidity 0.8

  # Low stress regime
  shortscreen-cli --downturn 0.2 --inflation 0.3 --liquidity 0.2

  # Show top 10 only
  shortscreen-cli --downturn 0.7 --inflation 0.6 --liquidity 0.5 --top 10
        """
    )

    parser.add_argument(
        '--downturn',
        type=float,
        required=True,
        help='Downturn risk indicator (0.0 - 1.0)'
    )
    parser.add_argument(
        '--inflation',
        type=float,
        required=True,
        help='Inflation pressure indicator (0.0 - 1.0)'
    )
    parser.add_argument(
        '--liquidity',
        type=float,
        required=True,
        help='Liquidity stress indicator (0.0 - 1.0)'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=20,
        help='Number of top candidates to display (default: 20)'
    )
    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Show only summary statistics, not individual candidates'
    )

    args = parser.parse_args()

    # Validate inputs
    try:
        macro_regime = MacroRegime(
            downturn=args.downturn,
            inflation=args.inflation,
            liquidity=args.liquidity
        )
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Run the engine
    print("\nRunning ShortScreen engine...", file=sys.stderr)
    engine = ShortScreenEngine()
    candidates = engine.run(macro_regime)

    # Print summary
    print_summary(candidates, macro_regime)

    # Print top candidates
    if not args.summary_only:
        top_n = min(args.top, len(candidates))
        print(f"\n{'='*80}")
        print(f"TOP {top_n} SHORT CANDIDATES")
        print(f"{'='*80}")

        for i, candidate in enumerate(candidates[:top_n], 1):
            print(format_candidate(candidate, i))

    print("\n" + "="*80 + "\n")


if __name__ == '__main__':
    main()
