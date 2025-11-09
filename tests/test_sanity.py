"""
Sanity tests for factor scoring logic.

These tests ensure that factor scores respond correctly to changes in metrics:
- Higher leverage increases leverage score
- Lower profitability increases profitability score
- Higher valuation increases valuation score
- Negative FCF increases quality score
"""

import pytest
from shortscreen.data import MarketData, FundamentalData
from shortscreen.factors import compute_raw_metrics, compute_factor_scores


def create_baseline_market_data(ticker: str) -> MarketData:
    """Create baseline market data for testing."""
    return MarketData(
        ticker=ticker,
        price=100.0,
        market_cap=1000.0,
        beta=1.0,
        volume_20d_avg=1000000.0,
        price_52w_high=120.0,
        price_52w_low=80.0
    )


def create_baseline_fundamental_data(ticker: str) -> FundamentalData:
    """Create baseline fundamental data for testing."""
    return FundamentalData(
        ticker=ticker,
        revenue=500.0,
        revenue_growth=0.10,
        ebitda=100.0,
        net_income=50.0,
        total_debt=200.0,
        cash=100.0,
        total_assets=1000.0,
        total_equity=500.0,
        free_cash_flow=40.0,
        shares_outstanding=10.0,
        sector="Technology",
        industry="Software"
    )


class TestSanityChecks:
    """Sanity tests for factor scoring."""

    def test_higher_leverage_increases_leverage_score(self):
        """Higher debt-to-equity should increase leverage score."""
        # Create two companies: low leverage and high leverage
        low_leverage_ticker = "LOW_LEV"
        high_leverage_ticker = "HIGH_LEV"

        # Low leverage company
        low_market = create_baseline_market_data(low_leverage_ticker)
        low_fund = create_baseline_fundamental_data(low_leverage_ticker)
        low_fund.total_debt = 100.0  # Low debt

        # High leverage company
        high_market = create_baseline_market_data(high_leverage_ticker)
        high_fund = create_baseline_fundamental_data(high_leverage_ticker)
        high_fund.total_debt = 500.0  # High debt

        # Compute raw metrics
        low_raw = compute_raw_metrics(low_leverage_ticker, low_market, low_fund)
        high_raw = compute_raw_metrics(high_leverage_ticker, high_market, high_fund)

        # Verify debt-to-equity is different
        assert high_raw.debt_to_equity > low_raw.debt_to_equity, \
            "High leverage company should have higher debt-to-equity"

        # Compute factor scores
        universe = [low_raw, high_raw]
        low_scores = compute_factor_scores(low_raw, universe)
        high_scores = compute_factor_scores(high_raw, universe)

        # Higher leverage should have higher leverage score
        assert high_scores.leverage_score > low_scores.leverage_score, \
            "Higher leverage should result in higher leverage score"

        print(f"✓ Leverage sanity check passed:")
        print(f"  Low D/E: {low_raw.debt_to_equity:.2f} → Score: {low_scores.leverage_score:.1f}")
        print(f"  High D/E: {high_raw.debt_to_equity:.2f} → Score: {high_scores.leverage_score:.1f}")

    def test_lower_profitability_increases_profitability_score(self):
        """Lower profitability should increase profitability score (more bearish)."""
        # Create a universe of companies with varying profitability
        universe = []

        # Create 10 companies with different profitability levels
        for i in range(10):
            ticker = f"COMPANY_{i}"
            market = create_baseline_market_data(ticker)
            fund = create_baseline_fundamental_data(ticker)
            # Vary profitability from -10% to +20%
            fund.net_income = fund.revenue * (-0.10 + i * 0.03)
            fund.ebitda = fund.revenue * (0.0 + i * 0.03)
            raw = compute_raw_metrics(ticker, market, fund)
            universe.append(raw)

        # Get the most profitable and least profitable
        prof_raw = universe[-1]  # Highest profit
        unprof_raw = universe[0]  # Lowest profit (negative)

        # Verify margins are different
        assert prof_raw.net_margin > unprof_raw.net_margin, \
            "Profitable company should have higher margin"

        # Compute factor scores
        prof_scores = compute_factor_scores(prof_raw, universe)
        unprof_scores = compute_factor_scores(unprof_raw, universe)

        # Debug: print actual values
        print(f"DEBUG Profitability test:")
        print(f"  Profitable: margin={prof_raw.net_margin:.2%}, score={prof_scores.profitability_score:.1f}")
        print(f"  Unprofitable: margin={unprof_raw.net_margin:.2%}, score={unprof_scores.profitability_score:.1f}")

        # Lower profitability should have higher score (because reverse=True)
        assert unprof_scores.profitability_score > prof_scores.profitability_score, \
            f"Lower profitability should result in higher profitability score: {unprof_scores.profitability_score:.1f} vs {prof_scores.profitability_score:.1f}"

        print(f"✓ Profitability sanity check passed:")
        print(f"  High margin: {prof_raw.net_margin:.2%} → Score: {prof_scores.profitability_score:.1f}")
        print(f"  Low margin: {unprof_raw.net_margin:.2%} → Score: {unprof_scores.profitability_score:.1f}")

    def test_higher_valuation_increases_valuation_score(self):
        """Higher valuation multiples should increase valuation score."""
        cheap_ticker = "CHEAP"
        expensive_ticker = "EXPENSIVE"

        # Cheap company (low market cap, high fundamentals)
        cheap_market = create_baseline_market_data(cheap_ticker)
        cheap_market.market_cap = 500.0  # Low valuation
        cheap_fund = create_baseline_fundamental_data(cheap_ticker)

        # Expensive company (high market cap, same fundamentals)
        exp_market = create_baseline_market_data(expensive_ticker)
        exp_market.market_cap = 5000.0  # High valuation
        exp_fund = create_baseline_fundamental_data(expensive_ticker)

        # Compute raw metrics
        cheap_raw = compute_raw_metrics(cheap_ticker, cheap_market, cheap_fund)
        exp_raw = compute_raw_metrics(expensive_ticker, exp_market, exp_fund)

        # Verify P/S is different
        assert exp_raw.price_to_sales > cheap_raw.price_to_sales, \
            "Expensive company should have higher P/S"

        # Compute factor scores
        universe = [cheap_raw, exp_raw]
        cheap_scores = compute_factor_scores(cheap_raw, universe)
        exp_scores = compute_factor_scores(exp_raw, universe)

        # Higher valuation should have higher score
        assert exp_scores.valuation_score > cheap_scores.valuation_score, \
            "Higher valuation should result in higher valuation score"

        print(f"✓ Valuation sanity check passed:")
        print(f"  Low P/S: {cheap_raw.price_to_sales:.2f} → Score: {cheap_scores.valuation_score:.1f}")
        print(f"  High P/S: {exp_raw.price_to_sales:.2f} → Score: {exp_scores.valuation_score:.1f}")

    def test_negative_fcf_increases_quality_score(self):
        """Negative free cash flow should increase quality score (more bearish)."""
        good_quality_ticker = "GOOD_QUALITY"
        bad_quality_ticker = "BAD_QUALITY"

        # Good quality (positive FCF)
        good_market = create_baseline_market_data(good_quality_ticker)
        good_fund = create_baseline_fundamental_data(good_quality_ticker)
        good_fund.free_cash_flow = 100.0  # Strong FCF

        # Bad quality (negative FCF)
        bad_market = create_baseline_market_data(bad_quality_ticker)
        bad_fund = create_baseline_fundamental_data(bad_quality_ticker)
        bad_fund.free_cash_flow = -50.0  # Burning cash

        # Compute raw metrics
        good_raw = compute_raw_metrics(good_quality_ticker, good_market, good_fund)
        bad_raw = compute_raw_metrics(bad_quality_ticker, bad_market, bad_fund)

        # Verify FCF margin is different
        assert good_raw.fcf_margin > bad_raw.fcf_margin, \
            "Good quality company should have higher FCF margin"

        # Compute factor scores
        universe = [good_raw, bad_raw]
        good_scores = compute_factor_scores(good_raw, universe)
        bad_scores = compute_factor_scores(bad_raw, universe)

        # Negative FCF should have higher quality score (more bearish)
        assert bad_scores.quality_score > good_scores.quality_score, \
            "Negative FCF should result in higher quality score"

        print(f"✓ Quality sanity check passed:")
        print(f"  Positive FCF: {good_raw.fcf_margin:.2%} → Score: {good_scores.quality_score:.1f}")
        print(f"  Negative FCF: {bad_raw.fcf_margin:.2%} → Score: {bad_scores.quality_score:.1f}")

    def test_negative_growth_increases_growth_score(self):
        """Negative revenue growth should increase growth score (more bearish)."""
        growing_ticker = "GROWING"
        declining_ticker = "DECLINING"

        # Growing company
        growing_market = create_baseline_market_data(growing_ticker)
        growing_fund = create_baseline_fundamental_data(growing_ticker)
        growing_fund.revenue_growth = 0.30  # 30% growth

        # Declining company
        declining_market = create_baseline_market_data(declining_ticker)
        declining_fund = create_baseline_fundamental_data(declining_ticker)
        declining_fund.revenue_growth = -0.15  # -15% decline

        # Compute raw metrics
        growing_raw = compute_raw_metrics(growing_ticker, growing_market, growing_fund)
        declining_raw = compute_raw_metrics(declining_ticker, declining_market, declining_fund)

        # Compute factor scores
        universe = [growing_raw, declining_raw]
        growing_scores = compute_factor_scores(growing_raw, universe)
        declining_scores = compute_factor_scores(declining_raw, universe)

        # Declining should have higher growth score
        assert declining_scores.growth_score > growing_scores.growth_score, \
            "Negative growth should result in higher growth score"

        print(f"✓ Growth sanity check passed:")
        print(f"  High growth: {growing_raw.revenue_growth:.1%} → Score: {growing_scores.growth_score:.1f}")
        print(f"  Declining: {declining_raw.revenue_growth:.1%} → Score: {declining_scores.growth_score:.1f}")


if __name__ == "__main__":
    # Run sanity checks
    test = TestSanityChecks()
    print("\nRunning sanity checks...\n")

    test.test_higher_leverage_increases_leverage_score()
    test.test_lower_profitability_increases_profitability_score()
    test.test_higher_valuation_increases_valuation_score()
    test.test_negative_fcf_increases_quality_score()
    test.test_negative_growth_increases_growth_score()

    print("\n✓ All sanity checks passed!")
