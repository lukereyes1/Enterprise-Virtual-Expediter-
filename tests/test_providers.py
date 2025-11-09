"""
Unit tests for data providers.

These tests verify provider logic using mocks to avoid requiring real API access.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from shortscreen.providers.base import (
    BaseProvider,
    ProviderHealth,
    ProviderStatus,
    ProviderError
)
from shortscreen.providers.yfinance_provider import YahooFinanceProvider
from shortscreen.providers.alphavantage_provider import AlphaVantageProvider
from shortscreen.providers.manager import ProviderManager
from shortscreen.models.data import MarketData, FundamentalData


class TestYahooFinanceProvider:
    """Tests for Yahoo Finance provider."""

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.yfinance_provider.yf')
    def test_get_market_data_success(self, mock_yf):
        """Test successful market data fetch."""
        # Mock yfinance response
        mock_ticker = Mock()
        mock_ticker.info = {
            'currentPrice': 150.0,
            'marketCap': 2500000000000,  # $2.5T
            'beta': 1.2,
            'averageVolume': 50000000,
            'fiftyTwoWeekHigh': 180.0,
            'fiftyTwoWeekLow': 120.0,
        }
        mock_yf.Ticker.return_value = mock_ticker

        provider = YahooFinanceProvider()
        data = provider.get_market_data('AAPL')

        assert data.ticker == 'AAPL'
        assert data.price == 150.0
        assert data.market_cap == 2500000.0  # In millions
        assert data.beta == 1.2
        assert data.volume_20d_avg == 50000000
        assert data.price_52w_high == 180.0
        assert data.price_52w_low == 120.0

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.yfinance_provider.yf')
    def test_get_fundamental_data_success(self, mock_yf):
        """Test successful fundamental data fetch."""
        # Mock yfinance response
        mock_ticker = Mock()
        mock_ticker.info = {
            'totalRevenue': 365000000000,
            'revenueGrowth': 0.08,
            'ebitda': 120000000000,
            'netIncomeToCommon': 95000000000,
            'freeCashflow': 100000000000,
            'totalDebt': 110000000000,
            'totalCash': 50000000000,
            'totalAssets': 350000000000,
            'totalStockholderEquity': 60000000000,
            'sharesOutstanding': 16000000000,
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
        }
        mock_yf.Ticker.return_value = mock_ticker

        provider = YahooFinanceProvider()
        data = provider.get_fundamental_data('AAPL')

        assert data.ticker == 'AAPL'
        assert data.revenue == 365000.0  # In millions
        assert data.revenue_growth == 0.08
        assert data.ebitda == 120000.0
        assert data.net_income == 95000.0
        assert data.free_cash_flow == 100000.0
        assert data.total_debt == 110000.0
        assert data.cash == 50000.0
        assert data.total_assets == 350000.0
        assert data.total_equity == 60000.0
        assert data.shares_outstanding == 16000.0
        assert data.sector == 'Technology'
        assert data.industry == 'Consumer Electronics'

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.yfinance_provider.yf')
    def test_retry_on_failure(self, mock_yf):
        """Test retry logic on API failure."""
        # First ticker instance fails, second succeeds
        failing_ticker = Mock()
        failing_ticker.info = Mock(side_effect=Exception("Network error"))

        success_ticker = Mock()
        success_ticker.info = {
            'currentPrice': 150.0,
            'marketCap': 2500000000000,
            'beta': 1.2,
            'averageVolume': 50000000,
            'fiftyTwoWeekHigh': 180.0,
            'fiftyTwoWeekLow': 120.0,
        }

        # First call returns failing ticker, second returns success ticker
        mock_yf.Ticker.side_effect = [failing_ticker, success_ticker]

        provider = YahooFinanceProvider(config={'retry_attempts': 2, 'retry_delay_seconds': 0.1})

        # Should succeed on retry
        with patch('time.sleep'):  # Don't actually sleep in tests
            data = provider.get_market_data('AAPL')
            assert data.price == 150.0

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.yfinance_provider.yf')
    def test_all_retries_fail(self, mock_yf):
        """Test when all retry attempts fail."""
        mock_ticker = Mock()
        mock_ticker.info.side_effect = Exception("Persistent error")
        mock_yf.Ticker.return_value = mock_ticker

        provider = YahooFinanceProvider(config={'retry_attempts': 2, 'retry_delay_seconds': 0.1})

        with patch('time.sleep'):
            with pytest.raises(ProviderError):
                provider.get_market_data('AAPL')

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.yfinance_provider.yf')
    def test_health_check_healthy(self, mock_yf):
        """Test health check when provider is healthy."""
        # Mock successful responses
        mock_ticker = Mock()
        mock_ticker.info = {
            'currentPrice': 150.0,
            'marketCap': 2500000000000,
            'beta': 1.2,
            'averageVolume': 50000000,
            'fiftyTwoWeekHigh': 180.0,
            'fiftyTwoWeekLow': 120.0,
        }
        mock_yf.Ticker.return_value = mock_ticker

        provider = YahooFinanceProvider()
        health = provider.health_check()

        assert health.status == ProviderStatus.HEALTHY
        assert health.success_rate > 0.0
        assert health.avg_latency_ms >= 0.0
        assert len(health.errors) == 0

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.yfinance_provider.yf')
    def test_health_check_unhealthy(self, mock_yf):
        """Test health check when provider is unhealthy."""
        # Mock failing responses
        mock_ticker = Mock()
        mock_ticker.info.side_effect = Exception("API down")
        mock_yf.Ticker.return_value = mock_ticker

        provider = YahooFinanceProvider(config={'retry_attempts': 1, 'retry_delay_seconds': 0.1})

        with patch('time.sleep'):
            health = provider.health_check()

        assert health.status == ProviderStatus.UNHEALTHY
        assert health.success_rate == 0.0
        assert len(health.errors) > 0


class TestAlphaVantageProvider:
    """Tests for Alpha Vantage provider."""

    def test_not_implemented(self):
        """Test that Alpha Vantage methods raise NotImplementedError."""
        provider = AlphaVantageProvider(config={'api_key': 'test_key'})

        with pytest.raises(NotImplementedError):
            provider.get_universe()

        with pytest.raises(NotImplementedError):
            provider.get_market_data('AAPL')

        with pytest.raises(NotImplementedError):
            provider.get_fundamental_data('AAPL')

    def test_health_check_no_api_key(self):
        """Test health check without API key."""
        provider = AlphaVantageProvider()
        health = provider.health_check()

        assert health.status == ProviderStatus.UNHEALTHY
        assert 'API key not configured' in health.errors

    def test_health_check_with_api_key(self):
        """Test health check with API key (but not implemented)."""
        provider = AlphaVantageProvider(config={'api_key': 'test_key'})
        health = provider.health_check()

        assert health.status == ProviderStatus.UNKNOWN
        assert 'Health check not implemented' in health.errors


class TestProviderManager:
    """Tests for ProviderManager."""

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.manager.YahooFinanceProvider')
    def test_initialization(self, mock_yf_class):
        """Test provider manager initialization."""
        # Mock provider instance
        mock_provider = Mock()
        mock_yf_class.return_value = mock_provider

        manager = ProviderManager()

        # Should have initialized providers based on config
        assert len(manager.providers) > 0

    @patch('shortscreen.providers.yfinance_provider.yf')
    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    def test_get_market_data_with_fallback(self, mock_yf):
        """Test market data fetch with fallback."""
        # Mock yfinance
        mock_ticker = Mock()
        mock_ticker.info = {
            'currentPrice': 150.0,
            'marketCap': 2500000000000,
            'beta': 1.2,
            'averageVolume': 50000000,
            'fiftyTwoWeekHigh': 180.0,
            'fiftyTwoWeekLow': 120.0,
        }
        mock_yf.Ticker.return_value = mock_ticker

        manager = ProviderManager()
        data = manager.get_market_data('AAPL')

        assert data.ticker == 'AAPL'
        assert data.price == 150.0

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.manager.YahooFinanceProvider')
    def test_fallback_on_provider_failure(self, mock_yf_class):
        """Test fallback when first provider fails."""
        # Create two mock providers
        failing_provider = Mock(spec=YahooFinanceProvider)
        failing_provider.get_market_data.side_effect = Exception("Provider 1 failed")

        success_provider = Mock(spec=YahooFinanceProvider)
        success_provider.get_market_data.return_value = MarketData(
            ticker='AAPL',
            price=150.0,
            market_cap=2500000.0,
            beta=1.2,
            volume_20d_avg=50000000,
            price_52w_high=180.0,
            price_52w_low=120.0
        )

        # Mock provider initialization to return both providers
        mock_yf_class.side_effect = [failing_provider, success_provider]

        # Create manager with modified config that has two yahoo providers
        # (for testing purposes)
        manager = ProviderManager()
        manager.providers = [failing_provider, success_provider]

        data = manager.get_market_data('AAPL')

        # Should have fallen back to second provider
        assert data.ticker == 'AAPL'
        assert failing_provider.get_market_data.called
        assert success_provider.get_market_data.called

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.manager.YahooFinanceProvider')
    def test_all_providers_fail(self, mock_yf_class):
        """Test when all providers fail."""
        mock_provider = Mock(spec=YahooFinanceProvider)
        mock_provider.get_market_data.side_effect = Exception("All failed")
        mock_yf_class.return_value = mock_provider

        manager = ProviderManager()

        with pytest.raises(ProviderError) as exc_info:
            manager.get_market_data('AAPL')

        assert 'All providers failed' in str(exc_info.value)

    @patch('shortscreen.providers.yfinance_provider.yf')
    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    def test_health_check_all(self, mock_yf):
        """Test health check across all providers."""
        # Mock yfinance for health check
        mock_ticker = Mock()
        mock_ticker.info = {
            'currentPrice': 150.0,
            'marketCap': 2500000000000,
            'beta': 1.2,
            'averageVolume': 50000000,
            'fiftyTwoWeekHigh': 180.0,
            'fiftyTwoWeekLow': 120.0,
        }
        mock_yf.Ticker.return_value = mock_ticker

        manager = ProviderManager()
        health_results = manager.health_check_all()

        assert len(health_results) > 0
        assert any(h.status == ProviderStatus.HEALTHY for h in health_results.values())

    @patch('shortscreen.providers.yfinance_provider.YFINANCE_AVAILABLE', True)
    @patch('shortscreen.providers.manager.YahooFinanceProvider')
    def test_get_provider_status(self, mock_yf_class):
        """Test getting provider status."""
        mock_provider = Mock(spec=YahooFinanceProvider)
        mock_provider.health_check.return_value = ProviderHealth(
            status=ProviderStatus.HEALTHY,
            last_check=datetime.now(),
            success_rate=0.95,
            avg_latency_ms=150.0,
            errors=[]
        )
        mock_provider.__class__.__name__ = 'YahooFinanceProvider'
        mock_yf_class.return_value = mock_provider

        manager = ProviderManager()
        status = manager.get_provider_status()

        assert len(status) > 0
        for provider_name, info in status.items():
            assert 'priority' in info
            assert 'status' in info
            assert 'success_rate' in info
            assert 'avg_latency_ms' in info


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
