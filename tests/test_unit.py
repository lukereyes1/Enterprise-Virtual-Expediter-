"""
Unit tests for individual modules.
"""

import pytest
from shortscreen.macro import MacroRegime, compute_theme_weights
from shortscreen.data import DataProvider
from shortscreen.factors import percentile_rank


class TestMacroRegime:
    """Tests for MacroRegime."""

    def test_valid_regime(self):
        """Test creating a valid macro regime."""
        regime = MacroRegime(downturn=0.5, inflation=0.6, liquidity=0.7)
        assert regime.downturn == 0.5
        assert regime.inflation == 0.6
        assert regime.liquidity == 0.7

    def test_invalid_regime_too_high(self):
        """Test that values > 1.0 are rejected."""
        with pytest.raises(ValueError):
            MacroRegime(downturn=1.5, inflation=0.5, liquidity=0.5)

    def test_invalid_regime_too_low(self):
        """Test that values < 0.0 are rejected."""
        with pytest.raises(ValueError):
            MacroRegime(downturn=-0.1, inflation=0.5, liquidity=0.5)

    def test_boundary_values(self):
        """Test boundary values 0.0 and 1.0."""
        regime = MacroRegime(downturn=0.0, inflation=1.0, liquidity=0.5)
        assert regime.downturn == 0.0
        assert regime.inflation == 1.0


class TestThemeWeights:
    """Tests for theme weight computation."""

    def test_weights_sum_to_one(self):
        """Test that computed weights sum to 1.0."""
        regime = MacroRegime(downturn=0.7, inflation=0.6, liquidity=0.5)
        weights = compute_theme_weights(regime)

        total = sum(weights.values())
        assert abs(total - 1.0) < 1e-10, f"Weights sum to {total}, not 1.0"

    def test_all_weights_positive(self):
        """Test that all weights are non-negative."""
        regime = MacroRegime(downturn=0.8, inflation=0.9, liquidity=0.7)
        weights = compute_theme_weights(regime)

        for theme, weight in weights.items():
            assert weight >= 0, f"{theme} has negative weight: {weight}"

    def test_high_downturn_increases_most_sensitive_theme(self):
        """Test that themes respond correctly to macro regime changes."""
        low_downturn = MacroRegime(downturn=0.1, inflation=0.5, liquidity=0.5)
        high_downturn = MacroRegime(downturn=0.9, inflation=0.5, liquidity=0.5)

        low_weights = compute_theme_weights(low_downturn)
        high_weights = compute_theme_weights(high_downturn)

        # High beta consumer has highest downturn sensitivity (0.7)
        # so it should increase the most when downturn increases
        assert high_weights['highbeta_consumer'] > low_weights['highbeta_consumer']

        # Unprofitable growth has low downturn sensitivity (0.2)
        # so it should increase less than average (decrease after normalization)
        assert high_weights['unprofitable_growth'] < low_weights['unprofitable_growth']


class TestDataProvider:
    """Tests for DataProvider."""

    def test_get_universe_returns_tickers(self):
        """Test that get_universe returns a list of tickers."""
        provider = DataProvider(use_mock=True)
        universe = provider.get_universe()

        assert isinstance(universe, list)
        assert len(universe) > 0
        assert all(isinstance(ticker, str) for ticker in universe)

    def test_get_market_data(self):
        """Test that get_market_data returns valid data."""
        provider = DataProvider(use_mock=True)
        data = provider.get_market_data("TEST")

        assert data.ticker == "TEST"
        assert data.price > 0
        assert data.market_cap > 0
        assert data.beta > 0

    def test_get_fundamental_data(self):
        """Test that get_fundamental_data returns valid data."""
        provider = DataProvider(use_mock=True)
        data = provider.get_fundamental_data("TEST")

        assert data.ticker == "TEST"
        assert data.revenue > 0
        assert data.sector in ["Technology", "Financials", "Consumer Discretionary", "Industrials"]


class TestPercentileRank:
    """Tests for percentile_rank function."""

    def test_percentile_rank_basic(self):
        """Test basic percentile rank calculation."""
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # Minimum value should be ~0th percentile
        assert percentile_rank(1, values) < 15

        # Maximum value should be ~100th percentile
        assert percentile_rank(10, values) > 85

        # Median should be ~50th percentile
        median_rank = percentile_rank(5.5, values)
        assert 40 < median_rank < 60

    def test_percentile_rank_reverse(self):
        """Test reverse percentile ranking."""
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        # With reverse=True, highest value gets lowest percentile
        rank_high = percentile_rank(10, values, reverse=True)
        rank_low = percentile_rank(1, values, reverse=True)

        assert rank_high < rank_low

    def test_percentile_rank_empty_list(self):
        """Test percentile rank with empty list."""
        result = percentile_rank(5, [])
        assert result == 50.0  # Default to median


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
