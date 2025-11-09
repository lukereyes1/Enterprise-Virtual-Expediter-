"""
Alpha Vantage data provider.

Stub implementation for Alpha Vantage API. Requires API key to function.
"""

import os
import logging
from datetime import datetime
from typing import List, Dict, Optional

from shortscreen.models.data import MarketData, FundamentalData
from shortscreen.providers.base import (
    BaseProvider,
    ProviderHealth,
    ProviderStatus,
    ProviderError
)

logger = logging.getLogger(__name__)


class AlphaVantageProvider(BaseProvider):
    """
    Data provider for Alpha Vantage API.

    NOTE: This is a stub implementation. To use Alpha Vantage:
    1. Sign up for API key at https://www.alphavantage.co/support/#api-key
    2. Set environment variable: export ALPHA_VANTAGE_API_KEY=your_key_here
    3. Enable in data_providers.yaml
    """

    def __init__(self, config: Optional[Dict] = None):
        """Initialize Alpha Vantage provider."""
        super().__init__(config)

        # Get API key from config or environment
        self.api_key = self.config.get('api_key') or os.getenv('ALPHA_VANTAGE_API_KEY')

        if not self.api_key:
            logger.warning(
                "Alpha Vantage API key not found. "
                "Set ALPHA_VANTAGE_API_KEY environment variable."
            )

        self.timeout = self.config.get('timeout_seconds', 30)
        self.retry_attempts = self.config.get('retry_attempts', 3)
        self.retry_delay = self.config.get('retry_delay_seconds', 5)

        # Alpha Vantage has strict rate limits
        self.requests_per_minute = 5  # Free tier limit
        self.daily_request_limit = 500  # Free tier limit

    def get_universe(self, filters: Optional[Dict] = None) -> List[str]:
        """
        Get universe of tickers.

        Alpha Vantage doesn't provide a direct universe API.
        Would need to maintain separate ticker list.
        """
        raise NotImplementedError(
            "Alpha Vantage universe fetching not implemented. "
            "Use Yahoo Finance provider or provide ticker list directly."
        )

    def get_market_data(self, ticker: str) -> MarketData:
        """
        Fetch market data for a ticker.

        TODO: Implement using Alpha Vantage GLOBAL_QUOTE endpoint.
        """
        if not self.api_key:
            raise ProviderError("Alpha Vantage API key not configured")

        raise NotImplementedError(
            f"Alpha Vantage market data fetching not yet implemented for {ticker}. "
            "Contributions welcome! See: https://www.alphavantage.co/documentation/"
        )

    def get_fundamental_data(self, ticker: str) -> FundamentalData:
        """
        Fetch fundamental data for a ticker.

        TODO: Implement using Alpha Vantage OVERVIEW endpoint.
        """
        if not self.api_key:
            raise ProviderError("Alpha Vantage API key not configured")

        raise NotImplementedError(
            f"Alpha Vantage fundamental data fetching not yet implemented for {ticker}. "
            "Contributions welcome! See: https://www.alphavantage.co/documentation/"
        )

    def health_check(self) -> ProviderHealth:
        """Perform health check."""
        if not self.api_key:
            self._health = ProviderHealth(
                status=ProviderStatus.UNHEALTHY,
                last_check=datetime.now(),
                success_rate=0.0,
                avg_latency_ms=0.0,
                errors=["API key not configured"]
            )
        else:
            # TODO: Implement actual health check
            self._health = ProviderHealth(
                status=ProviderStatus.UNKNOWN,
                last_check=datetime.now(),
                success_rate=0.0,
                avg_latency_ms=0.0,
                errors=["Health check not implemented"]
            )

        return self._health


# Implementation guide for contributors:
# ======================================
#
# To implement Alpha Vantage support:
#
# 1. Install requests library: pip install requests
#
# 2. Use these API endpoints:
#    - GLOBAL_QUOTE: Real-time price data
#      https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo
#
#    - OVERVIEW: Company fundamentals
#      https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo
#
# 3. Handle rate limits:
#    - Free tier: 5 requests/minute, 500 requests/day
#    - Implement request throttling and queuing
#
# 4. Map Alpha Vantage fields to our data models:
#    MarketData fields:
#      - price: "05. price"
#      - volume_20d_avg: Calculate from TIME_SERIES_DAILY
#      - beta: Not available (use 1.0 as default)
#
#    FundamentalData fields:
#      - revenue: "RevenueTTM"
#      - ebitda: "EBITDA"
#      - total_debt: "TotalDebt"
#      - sector: "Sector"
#      - industry: "Industry"
#
# 5. Add comprehensive error handling for:
#    - API rate limit exceeded
#    - Invalid API key
#    - Network timeouts
#    - Invalid ticker symbols
#
# Example implementation structure:
#
# def _make_api_request(self, function: str, symbol: str) -> dict:
#     url = "https://www.alphavantage.co/query"
#     params = {
#         "function": function,
#         "symbol": symbol,
#         "apikey": self.api_key
#     }
#     response = requests.get(url, params=params, timeout=self.timeout)
#     response.raise_for_status()
#     return response.json()
