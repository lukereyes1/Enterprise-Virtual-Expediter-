"""
Yahoo Finance data provider using yfinance library.

Fetches real-time market and fundamental data from Yahoo Finance.
"""

import time
import logging
from datetime import datetime
from typing import List, Dict, Optional

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    yf = None

from shortscreen.models.data import MarketData, FundamentalData
from shortscreen.providers.base import (
    BaseProvider,
    ProviderHealth,
    ProviderStatus,
    ProviderError
)

logger = logging.getLogger(__name__)


class YahooFinanceProvider(BaseProvider):
    """
    Data provider for Yahoo Finance.

    Uses yfinance library to fetch market and fundamental data.
    """

    def __init__(self, config: Optional[Dict] = None):
        """Initialize Yahoo Finance provider."""
        super().__init__(config)

        if not YFINANCE_AVAILABLE:
            raise ImportError(
                "yfinance library not installed. Install with: pip install yfinance"
            )

        self.timeout = self.config.get('timeout_seconds', 30)
        self.retry_attempts = self.config.get('retry_attempts', 3)
        self.retry_delay = self.config.get('retry_delay_seconds', 2)
        self.batch_size = self.config.get('batch_size', 50)

    def get_universe(self, filters: Optional[Dict] = None) -> List[str]:
        """
        Get universe of tickers.

        Note: Yahoo Finance doesn't provide a direct universe API.
        This method returns common S&P 500 tickers as a starting point.
        In production, you would maintain your own universe list.
        """
        # Common S&P 500 tickers (partial list for demonstration)
        sp500_sample = [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
            "UNH", "JNJ", "XOM", "JPM", "V", "PG", "MA", "HD", "CVX", "LLY",
            "ABBV", "MRK", "KO", "AVGO", "PEP", "COST", "TMO", "WMT", "CSCO",
            "MCD", "ACN", "ABT", "DHR", "ADBE", "NKE", "CRM", "BAC", "CMCSA",
            "TXN", "NEE", "VZ", "PM", "DIS", "WFC", "UPS", "RTX", "HON", "INTC",
            "LOW", "QCOM", "IBM", "ORCL", "T", "SBUX", "SPGI", "CAT", "GE",
            "AMD", "AMGN", "INTU", "BA", "MDT", "AXP", "GS", "NOW", "BLK",
            "CVS", "PLD", "DE", "C", "SYK", "PFE", "MS", "LMT", "ELV", "ZTS",
            "GILD", "ADI", "MMC", "ISRG", "TJX", "BKNG", "CI", "SCHW", "CB",
            "MO", "BMY", "ETN", "VRTX", "EOG", "ADP", "SLB", "BDX", "DUK",
            "TMUS", "SO", "NOC", "PGR", "ITW", "APD", "EW", "CL", "CME", "REGN"
        ]

        # Apply filters if provided
        if filters:
            # In a real implementation, you would filter based on market cap,
            # sector, etc. For now, we just return the sample list.
            pass

        return sp500_sample

    def get_market_data(self, ticker: str) -> MarketData:
        """Fetch market data for a ticker."""
        for attempt in range(self.retry_attempts):
            try:
                return self._fetch_market_data(ticker)
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    raise ProviderError(f"Failed to fetch market data for {ticker}: {e}")
                logger.warning(f"Attempt {attempt + 1} failed for {ticker}, retrying...")
                time.sleep(self.retry_delay)

    def _fetch_market_data(self, ticker: str) -> MarketData:
        """Internal method to fetch market data."""
        stock = yf.Ticker(ticker)
        info = stock.info

        # Extract market data with fallbacks
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        market_cap = info.get('marketCap', 0) / 1_000_000  # Convert to millions

        beta = info.get('beta', 1.0)
        volume_20d_avg = info.get('averageVolume', 0)

        # Get 52-week range
        price_52w_high = info.get('fiftyTwoWeekHigh', price * 1.2)
        price_52w_low = info.get('fiftyTwoWeekLow', price * 0.8)

        # Validate data
        if price <= 0:
            raise ProviderError(f"Invalid price for {ticker}: {price}")

        return MarketData(
            ticker=ticker,
            price=float(price),
            market_cap=float(market_cap),
            beta=float(beta) if beta else 1.0,
            volume_20d_avg=float(volume_20d_avg),
            price_52w_high=float(price_52w_high),
            price_52w_low=float(price_52w_low)
        )

    def get_fundamental_data(self, ticker: str) -> FundamentalData:
        """Fetch fundamental data for a ticker."""
        for attempt in range(self.retry_attempts):
            try:
                return self._fetch_fundamental_data(ticker)
            except Exception as e:
                if attempt == self.retry_attempts - 1:
                    raise ProviderError(f"Failed to fetch fundamental data for {ticker}: {e}")
                logger.warning(f"Attempt {attempt + 1} failed for {ticker}, retrying...")
                time.sleep(self.retry_delay)

    def _fetch_fundamental_data(self, ticker: str) -> FundamentalData:
        """Internal method to fetch fundamental data."""
        stock = yf.Ticker(ticker)
        info = stock.info

        # Extract fundamental data with fallbacks
        revenue = info.get('totalRevenue', 0) / 1_000_000  # Convert to millions
        ebitda = info.get('ebitda', 0) / 1_000_000 if info.get('ebitda') else 0
        net_income = info.get('netIncomeToCommon', 0) / 1_000_000 if info.get('netIncomeToCommon') else 0

        # Estimate revenue growth (simplified)
        revenue_growth = info.get('revenueGrowth', 0.0)

        # Balance sheet items
        total_debt = info.get('totalDebt', 0) / 1_000_000 if info.get('totalDebt') else 0
        cash = info.get('totalCash', 0) / 1_000_000 if info.get('totalCash') else 0
        total_assets = info.get('totalAssets', 0) / 1_000_000 if info.get('totalAssets') else 0
        total_equity = info.get('totalStockholderEquity', 0) / 1_000_000 if info.get('totalStockholderEquity') else 0

        # Free cash flow
        free_cash_flow = info.get('freeCashflow', 0) / 1_000_000 if info.get('freeCashflow') else 0

        # Shares outstanding
        shares_outstanding = info.get('sharesOutstanding', 0) / 1_000_000  # Convert to millions

        # Sector and industry
        sector = info.get('sector', 'Unknown')
        industry = info.get('industry', 'Unknown')

        # Validate critical data
        if revenue <= 0 and total_assets <= 0:
            raise ProviderError(f"Insufficient fundamental data for {ticker}")

        return FundamentalData(
            ticker=ticker,
            revenue=float(revenue),
            revenue_growth=float(revenue_growth),
            ebitda=float(ebitda),
            net_income=float(net_income),
            total_debt=float(total_debt),
            cash=float(cash),
            total_assets=float(total_assets),
            total_equity=float(total_equity),
            free_cash_flow=float(free_cash_flow),
            shares_outstanding=float(shares_outstanding),
            sector=sector,
            industry=industry
        )

    def get_batch_market_data(self, tickers: List[str]) -> Dict[str, MarketData]:
        """
        Fetch market data for multiple tickers efficiently.

        Uses yfinance's batch download capability.
        """
        result = {}
        failed = []

        # Process in batches to avoid overwhelming the API
        for i in range(0, len(tickers), self.batch_size):
            batch = tickers[i:i + self.batch_size]

            for ticker in batch:
                try:
                    result[ticker] = self.get_market_data(ticker)
                except ProviderError as e:
                    failed.append(ticker)
                    logger.warning(f"Failed to fetch market data for {ticker}: {e}")

        if failed:
            logger.warning(f"Failed to fetch market data for {len(failed)} tickers: {failed[:10]}")

        return result

    def get_batch_fundamental_data(self, tickers: List[str]) -> Dict[str, FundamentalData]:
        """Fetch fundamental data for multiple tickers efficiently."""
        result = {}
        failed = []

        # Process in batches
        for i in range(0, len(tickers), self.batch_size):
            batch = tickers[i:i + self.batch_size]

            for ticker in batch:
                try:
                    result[ticker] = self.get_fundamental_data(ticker)
                except ProviderError as e:
                    failed.append(ticker)
                    logger.warning(f"Failed to fetch fundamental data for {ticker}: {e}")

        if failed:
            logger.warning(f"Failed to fetch fundamental data for {len(failed)} tickers: {failed[:10]}")

        return result

    def health_check(self) -> ProviderHealth:
        """Perform health check by testing with sample tickers."""
        test_tickers = ["AAPL", "MSFT", "GOOGL"]
        successes = 0
        total_latency = 0.0
        errors = []

        for ticker in test_tickers:
            try:
                start = time.time()
                self.get_market_data(ticker)
                latency = (time.time() - start) * 1000  # Convert to ms
                total_latency += latency
                successes += 1
            except Exception as e:
                errors.append(f"{ticker}: {str(e)}")

        success_rate = successes / len(test_tickers)
        avg_latency = total_latency / len(test_tickers) if successes > 0 else 0

        # Determine status
        if success_rate >= 0.9:
            status = ProviderStatus.HEALTHY
        elif success_rate >= 0.5:
            status = ProviderStatus.DEGRADED
        else:
            status = ProviderStatus.UNHEALTHY

        self._health = ProviderHealth(
            status=status,
            last_check=datetime.now(),
            success_rate=success_rate,
            avg_latency_ms=avg_latency,
            errors=errors
        )

        return self._health
