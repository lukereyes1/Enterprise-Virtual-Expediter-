"""
Base provider interface for data sources.

Defines the abstract interface that all data providers must implement.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass

from shortscreen.models.data import MarketData, FundamentalData


class ProviderStatus(str, Enum):
    """Health status of a data provider."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ProviderHealth:
    """Health check result for a provider."""
    status: ProviderStatus
    last_check: datetime
    success_rate: float  # 0.0-1.0
    avg_latency_ms: float
    errors: List[str]


class BaseProvider(ABC):
    """
    Abstract base class for data providers.

    All data providers must implement this interface to be used by the
    screening engine.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the provider.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        self._health = ProviderHealth(
            status=ProviderStatus.UNKNOWN,
            last_check=datetime.now(),
            success_rate=0.0,
            avg_latency_ms=0.0,
            errors=[]
        )

    @abstractmethod
    def get_universe(self, filters: Optional[Dict] = None) -> List[str]:
        """
        Get a universe of tickers based on filters.

        Args:
            filters: Optional dictionary of filters (e.g., min_market_cap, sectors)

        Returns:
            List of ticker symbols
        """
        pass

    @abstractmethod
    def get_market_data(self, ticker: str) -> MarketData:
        """
        Fetch market data for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            MarketData object with market metrics

        Raises:
            ProviderError: If data cannot be fetched
        """
        pass

    @abstractmethod
    def get_fundamental_data(self, ticker: str) -> FundamentalData:
        """
        Fetch fundamental data for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            FundamentalData object with fundamental metrics

        Raises:
            ProviderError: If data cannot be fetched
        """
        pass

    def get_batch_market_data(self, tickers: List[str]) -> Dict[str, MarketData]:
        """
        Fetch market data for multiple tickers.

        Default implementation calls get_market_data for each ticker.
        Providers may override for optimized batch fetching.

        Args:
            tickers: List of ticker symbols

        Returns:
            Dictionary mapping tickers to MarketData objects
        """
        result = {}
        for ticker in tickers:
            try:
                result[ticker] = self.get_market_data(ticker)
            except Exception as e:
                self._health.errors.append(f"{ticker}: {str(e)}")
        return result

    def get_batch_fundamental_data(self, tickers: List[str]) -> Dict[str, FundamentalData]:
        """
        Fetch fundamental data for multiple tickers.

        Default implementation calls get_fundamental_data for each ticker.
        Providers may override for optimized batch fetching.

        Args:
            tickers: List of ticker symbols

        Returns:
            Dictionary mapping tickers to FundamentalData objects
        """
        result = {}
        for ticker in tickers:
            try:
                result[ticker] = self.get_fundamental_data(ticker)
            except Exception as e:
                self._health.errors.append(f"{ticker}: {str(e)}")
        return result

    @abstractmethod
    def health_check(self) -> ProviderHealth:
        """
        Perform a health check on the provider.

        Returns:
            ProviderHealth object with current status
        """
        pass

    def get_health(self) -> ProviderHealth:
        """Get cached health status."""
        return self._health


class ProviderError(Exception):
    """Exception raised when a provider fails to fetch data."""
    pass
