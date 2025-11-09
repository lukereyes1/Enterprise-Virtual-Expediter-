#!/usr/bin/env python3
"""
Test script for real data providers.

This script tests the Yahoo Finance provider and ProviderManager with real API calls.
Run this to verify the data provider integration is working correctly.

Usage:
    python test_real_providers.py
"""

import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from shortscreen.providers import (
    YahooFinanceProvider,
    ProviderManager
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_yahoo_finance_provider():
    """Test Yahoo Finance provider directly."""
    print("\n" + "="*70)
    print("TEST 1: Yahoo Finance Provider - Direct Access")
    print("="*70 + "\n")

    provider = YahooFinanceProvider()

    # Test tickers
    test_tickers = ['AAPL', 'MSFT', 'GOOGL']

    for ticker in test_tickers:
        print(f"\nFetching data for {ticker}...")
        print("-" * 50)

        try:
            # Get market data
            market_data = provider.get_market_data(ticker)
            print(f"✓ Market Data:")
            print(f"  Price: ${market_data.price:.2f}")
            print(f"  Market Cap: ${market_data.market_cap:.2f}M")
            print(f"  Beta: {market_data.beta:.2f}")
            print(f"  Volume (20d avg): {market_data.volume_20d_avg:,.0f}")
            print(f"  52w High: ${market_data.high_52w:.2f}")
            print(f"  52w Low: ${market_data.low_52w:.2f}")

            # Get fundamental data
            fundamental_data = provider.get_fundamental_data(ticker)
            print(f"\n✓ Fundamental Data:")
            print(f"  Revenue: ${fundamental_data.revenue:.2f}M")
            print(f"  EBITDA: ${fundamental_data.ebitda:.2f}M")
            print(f"  Total Debt: ${fundamental_data.total_debt:.2f}M")
            print(f"  Cash: ${fundamental_data.cash:.2f}M")
            print(f"  Sector: {fundamental_data.sector}")
            print(f"  Industry: {fundamental_data.industry}")

        except Exception as e:
            print(f"✗ Error fetching {ticker}: {e}")

    # Test health check
    print("\n" + "-" * 50)
    print("Health Check:")
    print("-" * 50)
    health = provider.health_check()
    print(f"Status: {health.status.value}")
    print(f"Success Rate: {health.success_rate:.1%}")
    print(f"Avg Latency: {health.avg_latency_ms:.0f}ms")
    if health.errors:
        print(f"Errors: {health.errors}")


def test_provider_manager():
    """Test ProviderManager with automatic fallback."""
    print("\n" + "="*70)
    print("TEST 2: Provider Manager - Automatic Fallback")
    print("="*70 + "\n")

    manager = ProviderManager()

    # Check provider status
    print("Provider Status:")
    print("-" * 50)
    status = manager.get_provider_status()
    for provider_name, info in status.items():
        print(f"\n{provider_name}:")
        print(f"  Priority: {info['priority']}")
        print(f"  Status: {info['status']}")
        print(f"  Success Rate: {info['success_rate']:.1%}")
        print(f"  Avg Latency: {info['avg_latency_ms']:.0f}ms")

    # Test fetching data through manager
    print("\n" + "-" * 50)
    print("Fetching data through manager:")
    print("-" * 50)

    test_ticker = 'TSLA'
    print(f"\nFetching {test_ticker}...")

    try:
        market_data = manager.get_market_data(test_ticker)
        print(f"✓ Market data retrieved successfully")
        print(f"  Price: ${market_data.price:.2f}")
        print(f"  Market Cap: ${market_data.market_cap:.2f}M")

        fundamental_data = manager.get_fundamental_data(test_ticker)
        print(f"✓ Fundamental data retrieved successfully")
        print(f"  Sector: {fundamental_data.sector}")
        print(f"  Revenue: ${fundamental_data.revenue:.2f}M")

    except Exception as e:
        print(f"✗ Error: {e}")

    # Test with invalid ticker
    print("\n" + "-" * 50)
    print("Testing error handling with invalid ticker:")
    print("-" * 50)

    invalid_ticker = 'INVALID_XYZ123'
    print(f"\nFetching {invalid_ticker}...")

    try:
        market_data = manager.get_market_data(invalid_ticker)
        print(f"✓ Unexpectedly succeeded: {market_data}")
    except Exception as e:
        print(f"✓ Error handled correctly: {e}")


def test_batch_fetching():
    """Test batch fetching performance."""
    print("\n" + "="*70)
    print("TEST 3: Batch Fetching Performance")
    print("="*70 + "\n")

    provider = YahooFinanceProvider()
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']

    print(f"Fetching market data for {len(tickers)} tickers...")
    print("-" * 50)

    import time
    start_time = time.time()

    results = []
    for ticker in tickers:
        try:
            market_data = provider.get_market_data(ticker)
            results.append((ticker, market_data.price, market_data.market_cap))
            print(f"✓ {ticker}: ${market_data.price:.2f} (${market_data.market_cap:.0f}M)")
        except Exception as e:
            print(f"✗ {ticker}: {e}")

    elapsed = time.time() - start_time
    print(f"\n✓ Fetched {len(results)}/{len(tickers)} tickers in {elapsed:.2f}s")
    print(f"  Average: {elapsed/len(tickers):.2f}s per ticker")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("REAL DATA PROVIDER TESTS")
    print("="*70)
    print("\nThis will make real API calls to Yahoo Finance.")
    print("Press Ctrl+C to cancel, or Enter to continue...")

    try:
        input()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        return

    try:
        test_yahoo_finance_provider()
        test_provider_manager()
        test_batch_fetching()

        print("\n" + "="*70)
        print("ALL TESTS COMPLETED")
        print("="*70 + "\n")

    except KeyboardInterrupt:
        print("\n\nTests interrupted.")
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
