"""
Provider manager for data source selection and fallback.

This module manages multiple data providers, handles selection based on
priority and health, and provides automatic fallback when providers fail.
"""

import logging
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Type
from datetime import datetime

from shortscreen.models.data import MarketData, FundamentalData
from shortscreen.providers.base import (
    BaseProvider,
    ProviderHealth,
    ProviderStatus,
    ProviderError
)
from shortscreen.providers.yfinance_provider import YahooFinanceProvider
from shortscreen.providers.alphavantage_provider import AlphaVantageProvider

logger = logging.getLogger(__name__)


class ProviderManager:
    """
    Manages multiple data providers with automatic fallback.

    The manager loads provider configurations, initializes enabled providers,
    and routes data requests to the best available provider based on priority
    and health status.
    """

    # Registry of available provider classes
    PROVIDER_REGISTRY: Dict[str, Type[BaseProvider]] = {
        'yfinance': YahooFinanceProvider,
        'alphavantage': AlphaVantageProvider,
    }

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the provider manager.

        Args:
            config_path: Path to data_providers.yaml config file.
                        If None, uses default location.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'config' / 'data_providers.yaml'

        self.config_path = config_path
        self.config = self._load_config()
        self.providers: List[BaseProvider] = []
        self._initialize_providers()

    def _load_config(self) -> dict:
        """Load provider configuration from YAML."""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            return {'providers': {}}

        with open(self.config_path) as f:
            config = yaml.safe_load(f)

        return config

    def _initialize_providers(self):
        """Initialize enabled providers based on configuration."""
        provider_configs = self.config.get('providers', {})

        # Sort by priority (lower number = higher priority)
        enabled_providers = [
            (name, cfg) for name, cfg in provider_configs.items()
            if cfg.get('enabled', False)
        ]
        enabled_providers.sort(key=lambda x: x[1].get('priority', 99))

        for name, cfg in enabled_providers:
            if name in self.PROVIDER_REGISTRY:
                try:
                    provider_class = self.PROVIDER_REGISTRY[name]
                    provider = provider_class(config=cfg)
                    self.providers.append(provider)
                    logger.info(f"Initialized {name} provider (priority {cfg.get('priority')})")
                except Exception as e:
                    logger.error(f"Failed to initialize {name} provider: {e}")
            else:
                logger.warning(f"Unknown provider type: {name}")

        if not self.providers:
            logger.warning("No data providers initialized! Using mock data fallback.")

    def get_universe(self, filters: Optional[Dict] = None) -> List[str]:
        """
        Get universe of tickers from the first available provider.

        Args:
            filters: Optional filters for universe selection

        Returns:
            List of ticker symbols

        Raises:
            ProviderError: If all providers fail
        """
        errors = []

        for provider in self.providers:
            try:
                logger.info(f"Fetching universe from {provider.__class__.__name__}")
                return provider.get_universe(filters)
            except NotImplementedError:
                logger.debug(f"{provider.__class__.__name__} doesn't support universe fetching")
                continue
            except Exception as e:
                logger.warning(f"{provider.__class__.__name__} failed: {e}")
                errors.append(f"{provider.__class__.__name__}: {str(e)}")
                continue

        raise ProviderError(
            f"All providers failed to fetch universe. Errors: {'; '.join(errors)}"
        )

    def get_market_data(self, ticker: str) -> MarketData:
        """
        Get market data for a ticker with automatic fallback.

        Tries providers in priority order until one succeeds.

        Args:
            ticker: Stock ticker symbol

        Returns:
            MarketData for the ticker

        Raises:
            ProviderError: If all providers fail
        """
        errors = []

        for provider in self.providers:
            try:
                logger.debug(f"Fetching market data for {ticker} from {provider.__class__.__name__}")
                return provider.get_market_data(ticker)
            except NotImplementedError:
                logger.debug(f"{provider.__class__.__name__} market data not implemented")
                continue
            except Exception as e:
                logger.warning(f"{provider.__class__.__name__} failed for {ticker}: {e}")
                errors.append(f"{provider.__class__.__name__}: {str(e)}")
                continue

        raise ProviderError(
            f"All providers failed to fetch market data for {ticker}. Errors: {'; '.join(errors)}"
        )

    def get_fundamental_data(self, ticker: str) -> FundamentalData:
        """
        Get fundamental data for a ticker with automatic fallback.

        Tries providers in priority order until one succeeds.

        Args:
            ticker: Stock ticker symbol

        Returns:
            FundamentalData for the ticker

        Raises:
            ProviderError: If all providers fail
        """
        errors = []

        for provider in self.providers:
            try:
                logger.debug(f"Fetching fundamental data for {ticker} from {provider.__class__.__name__}")
                return provider.get_fundamental_data(ticker)
            except NotImplementedError:
                logger.debug(f"{provider.__class__.__name__} fundamental data not implemented")
                continue
            except Exception as e:
                logger.warning(f"{provider.__class__.__name__} failed for {ticker}: {e}")
                errors.append(f"{provider.__class__.__name__}: {str(e)}")
                continue

        raise ProviderError(
            f"All providers failed to fetch fundamental data for {ticker}. Errors: {'; '.join(errors)}"
        )

    def health_check_all(self) -> Dict[str, ProviderHealth]:
        """
        Perform health check on all providers.

        Returns:
            Dictionary mapping provider names to their health status
        """
        results = {}

        for provider in self.providers:
            provider_name = provider.__class__.__name__
            try:
                health = provider.health_check()
                results[provider_name] = health
                logger.info(
                    f"{provider_name} health: {health.status.value}, "
                    f"success_rate={health.success_rate:.1%}"
                )
            except Exception as e:
                logger.error(f"Health check failed for {provider_name}: {e}")
                results[provider_name] = ProviderHealth(
                    status=ProviderStatus.UNHEALTHY,
                    last_check=datetime.now(),
                    success_rate=0.0,
                    avg_latency_ms=0.0,
                    errors=[str(e)]
                )

        return results

    def get_healthy_providers(self) -> List[BaseProvider]:
        """
        Get list of providers that are currently healthy.

        Returns:
            List of healthy providers in priority order
        """
        healthy = []

        for provider in self.providers:
            health = provider.health_check()
            if health.status == ProviderStatus.HEALTHY:
                healthy.append(provider)

        return healthy

    def get_provider_status(self) -> Dict[str, dict]:
        """
        Get detailed status information for all providers.

        Returns:
            Dictionary with provider names and their detailed status
        """
        status = {}

        for i, provider in enumerate(self.providers):
            provider_name = provider.__class__.__name__
            health = provider.health_check()

            status[provider_name] = {
                'priority': i + 1,
                'status': health.status.value,
                'success_rate': health.success_rate,
                'avg_latency_ms': health.avg_latency_ms,
                'last_check': health.last_check.isoformat() if health.last_check else None,
                'errors': health.errors
            }

        return status
