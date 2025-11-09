"""
Data provider module for market and fundamental data access.

This module provides an abstraction layer for accessing market data, fundamental
metrics, and other data sources. The current implementation uses mock data for
testing and development, but is designed to be easily swapped with real API calls.
"""

from typing import List, Dict, Optional
import random
import hashlib

# Import models from central location (single source of truth)
from shortscreen.models.data import MarketData, FundamentalData


def _deterministic_hash(s: str) -> int:
    """
    Generate a deterministic hash from a string.

    Uses SHA-256 to avoid Python's PYTHONHASHSEED randomization which makes
    the built-in hash() function return different values across processes.

    Args:
        s: String to hash

    Returns:
        Deterministic integer hash value
    """
    # Use SHA-256 for deterministic hashing
    hash_bytes = hashlib.sha256(s.encode('utf-8')).digest()
    # Convert first 4 bytes to integer
    return int.from_bytes(hash_bytes[:4], byteorder='big')


class DataProvider:
    """
    Abstraction layer for market and fundamental data access.

    This class provides methods to fetch market and fundamental data for tickers.
    The current implementation returns mock data, but methods are designed to be
    easily replaced with real API calls (e.g., Yahoo Finance, Alpha Vantage, etc.).
    """

    def __init__(self, use_mock: bool = True):
        """
        Initialize the data provider.

        Args:
            use_mock: If True, use mock data. If False, use real API calls.
        """
        self.use_mock = use_mock
        random.seed(42)  # For reproducible mock data

    def get_universe(self, filters: Optional[Dict] = None) -> List[str]:
        """
        Get a universe of tickers based on filters.

        Args:
            filters: Optional dictionary of filters (e.g., min_market_cap, sectors)

        Returns:
            List of ticker symbols
        """
        if self.use_mock:
            # Mock universe of tickers
            return self._get_mock_universe(filters)
        else:
            # TODO: Implement real API call to fetch universe
            raise NotImplementedError("Real API calls not yet implemented")

    def get_market_data(self, ticker: str) -> MarketData:
        """
        Fetch market data for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            MarketData object with market metrics
        """
        if self.use_mock:
            return self._get_mock_market_data(ticker)
        else:
            # TODO: Implement real API call (e.g., yfinance, Alpha Vantage)
            raise NotImplementedError("Real API calls not yet implemented")

    def get_fundamental_data(self, ticker: str) -> FundamentalData:
        """
        Fetch fundamental data for a ticker.

        Args:
            ticker: Stock ticker symbol

        Returns:
            FundamentalData object with fundamental metrics
        """
        if self.use_mock:
            return self._get_mock_fundamental_data(ticker)
        else:
            # TODO: Implement real API call (e.g., Financial Modeling Prep, IEX Cloud)
            raise NotImplementedError("Real API calls not yet implemented")

    def get_batch_market_data(self, tickers: List[str]) -> Dict[str, MarketData]:
        """
        Fetch market data for multiple tickers.

        Args:
            tickers: List of ticker symbols

        Returns:
            Dictionary mapping tickers to MarketData objects
        """
        return {ticker: self.get_market_data(ticker) for ticker in tickers}

    def get_batch_fundamental_data(self, tickers: List[str]) -> Dict[str, FundamentalData]:
        """
        Fetch fundamental data for multiple tickers.

        Args:
            tickers: List of ticker symbols

        Returns:
            Dictionary mapping tickers to FundamentalData objects
        """
        return {ticker: self.get_fundamental_data(ticker) for ticker in tickers}

    # Mock data methods

    def _get_mock_universe(self, filters: Optional[Dict] = None) -> List[str]:
        """Generate a mock universe of tickers."""
        # Create a diverse set of mock tickers
        growth_tickers = [f"GROW{i}" for i in range(1, 26)]
        smallcap_tickers = [f"SMCAP{i}" for i in range(1, 26)]
        consumer_tickers = [f"CONS{i}" for i in range(1, 26)]
        financial_tickers = [f"FIN{i}" for i in range(1, 26)]

        all_tickers = growth_tickers + smallcap_tickers + consumer_tickers + financial_tickers

        # Apply filters if provided
        if filters:
            # For mock data, just return all tickers
            # In real implementation, filter based on criteria
            pass

        return all_tickers

    def _get_mock_market_data(self, ticker: str) -> MarketData:
        """Generate mock market data for a ticker."""
        # Use deterministic hash for consistent random data across runs
        seed = _deterministic_hash(ticker) % 10000
        random.seed(seed)

        price = random.uniform(10, 500)
        market_cap = random.uniform(100, 50000)  # $100M to $50B
        beta = random.uniform(0.5, 2.5)
        volume = random.uniform(100000, 10000000)

        return MarketData(
            ticker=ticker,
            price=price,
            market_cap=market_cap,
            beta=beta,
            volume_20d_avg=volume,
            price_52w_high=price * random.uniform(1.0, 1.8),
            price_52w_low=price * random.uniform(0.5, 1.0)
        )

    def _get_mock_fundamental_data(self, ticker: str) -> FundamentalData:
        """Generate mock fundamental data for a ticker."""
        # Use deterministic hash for consistent random data across runs
        seed = _deterministic_hash(ticker) % 10000
        random.seed(seed)

        # Determine sector based on ticker prefix
        if ticker.startswith("GROW"):
            sector = "Technology"
            industry = "Software"
        elif ticker.startswith("SMCAP"):
            sector = "Industrials"
            industry = "Manufacturing"
        elif ticker.startswith("CONS"):
            sector = "Consumer Discretionary"
            industry = "Retail"
        elif ticker.startswith("FIN"):
            sector = "Financials"
            industry = "Banks"
        else:
            sector = "Technology"
            industry = "Software"

        revenue = random.uniform(100, 10000)
        revenue_growth = random.uniform(-0.2, 0.8)
        ebitda = revenue * random.uniform(-0.1, 0.3)
        net_income = ebitda * random.uniform(-0.5, 0.8)
        total_debt = revenue * random.uniform(0.1, 3.0)
        cash = revenue * random.uniform(0.1, 0.5)
        total_assets = revenue * random.uniform(1.0, 5.0)
        total_equity = total_assets * random.uniform(0.2, 0.7)
        fcf = net_income * random.uniform(-0.5, 1.5)
        shares = random.uniform(50, 500)

        return FundamentalData(
            ticker=ticker,
            revenue=revenue,
            revenue_growth=revenue_growth,
            ebitda=ebitda,
            net_income=net_income,
            total_debt=total_debt,
            cash=cash,
            total_assets=total_assets,
            total_equity=total_equity,
            free_cash_flow=fcf,
            shares_outstanding=shares,
            sector=sector,
            industry=industry
        )
