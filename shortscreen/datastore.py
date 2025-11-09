"""
Data store module for caching and persistence.

Provides local caching for fundamentals and market data with freshness tracking.
Supports degraded mode when APIs are unavailable.
"""

import json
import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import pickle

from shortscreen.data import MarketData, FundamentalData

logger = logging.getLogger(__name__)


@dataclass
class CacheMetadata:
    """Metadata for cached data."""
    created_at: datetime
    updated_at: datetime
    data_source: str
    record_count: int
    version: str = "1.0"

    def is_stale(self, max_age: timedelta) -> bool:
        """Check if cache is stale based on max age."""
        age = datetime.now() - self.updated_at
        return age > max_age

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'data_source': self.data_source,
            'record_count': self.record_count,
            'version': self.version
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'CacheMetadata':
        """Create from dictionary."""
        return cls(
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            data_source=data['data_source'],
            record_count=data['record_count'],
            version=data.get('version', '1.0')
        )


class DataStore:
    """
    Local data store for caching market and fundamental data.

    Provides:
    - Separate caches for fundamentals (slow-changing) and market data (fast-changing)
    - Freshness tracking and staleness detection
    - Degraded mode support
    - Multiple storage formats (JSON, pickle, parquet)
    """

    def __init__(self, cache_dir: str = ".shortscreen_cache"):
        """
        Initialize data store.

        Args:
            cache_dir: Directory for cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Cache subdirectories
        self.fundamentals_dir = self.cache_dir / "fundamentals"
        self.market_data_dir = self.cache_dir / "market_data"
        self.results_dir = self.cache_dir / "results"

        for directory in [self.fundamentals_dir, self.market_data_dir, self.results_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        logger.info(f"DataStore initialized at {self.cache_dir}")

    # Fundamentals caching

    def save_fundamentals(
        self,
        data: Dict[str, FundamentalData],
        source: str = "api"
    ) -> None:
        """
        Save fundamental data to cache.

        Args:
            data: Dictionary mapping tickers to FundamentalData
            source: Data source identifier
        """
        cache_file = self.fundamentals_dir / "fundamentals.pkl"
        metadata_file = self.fundamentals_dir / "metadata.json"

        # Save data
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)

        # Save metadata
        metadata = CacheMetadata(
            created_at=datetime.now() if not metadata_file.exists() else self._load_metadata(metadata_file).created_at,
            updated_at=datetime.now(),
            data_source=source,
            record_count=len(data)
        )

        with open(metadata_file, 'w') as f:
            json.dump(metadata.to_dict(), f, indent=2)

        logger.info(f"Saved {len(data)} fundamental records to cache")

    def load_fundamentals(
        self,
        max_age: Optional[timedelta] = None
    ) -> Optional[Dict[str, FundamentalData]]:
        """
        Load fundamental data from cache.

        Args:
            max_age: Maximum age for cache validity. If None, load regardless of age.

        Returns:
            Dictionary of FundamentalData or None if cache is stale/missing
        """
        cache_file = self.fundamentals_dir / "fundamentals.pkl"
        metadata_file = self.fundamentals_dir / "metadata.json"

        if not cache_file.exists():
            logger.warning("Fundamentals cache not found")
            return None

        # Check metadata
        metadata = self._load_metadata(metadata_file)
        if metadata and max_age and metadata.is_stale(max_age):
            logger.warning(
                f"Fundamentals cache is stale (updated {metadata.updated_at}, "
                f"max age {max_age})"
            )
            return None

        # Load data
        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)

            logger.info(f"Loaded {len(data)} fundamental records from cache")
            return data
        except Exception as e:
            logger.error(f"Failed to load fundamentals cache: {e}")
            return None

    def get_fundamentals_metadata(self) -> Optional[CacheMetadata]:
        """Get metadata for fundamentals cache."""
        metadata_file = self.fundamentals_dir / "metadata.json"
        return self._load_metadata(metadata_file)

    # Market data caching

    def save_market_data(
        self,
        data: Dict[str, MarketData],
        source: str = "api"
    ) -> None:
        """
        Save market data to cache.

        Args:
            data: Dictionary mapping tickers to MarketData
            source: Data source identifier
        """
        cache_file = self.market_data_dir / "market_data.pkl"
        metadata_file = self.market_data_dir / "metadata.json"

        # Save data
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)

        # Save metadata
        metadata = CacheMetadata(
            created_at=datetime.now() if not metadata_file.exists() else self._load_metadata(metadata_file).created_at,
            updated_at=datetime.now(),
            data_source=source,
            record_count=len(data)
        )

        with open(metadata_file, 'w') as f:
            json.dump(metadata.to_dict(), f, indent=2)

        logger.info(f"Saved {len(data)} market data records to cache")

    def load_market_data(
        self,
        max_age: Optional[timedelta] = None
    ) -> Optional[Dict[str, MarketData]]:
        """
        Load market data from cache.

        Args:
            max_age: Maximum age for cache validity

        Returns:
            Dictionary of MarketData or None if cache is stale/missing
        """
        cache_file = self.market_data_dir / "market_data.pkl"
        metadata_file = self.market_data_dir / "metadata.json"

        if not cache_file.exists():
            logger.warning("Market data cache not found")
            return None

        # Check metadata
        metadata = self._load_metadata(metadata_file)
        if metadata and max_age and metadata.is_stale(max_age):
            logger.warning(
                f"Market data cache is stale (updated {metadata.updated_at}, "
                f"max age {max_age})"
            )
            return None

        # Load data
        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)

            logger.info(f"Loaded {len(data)} market data records from cache")
            return data
        except Exception as e:
            logger.error(f"Failed to load market data cache: {e}")
            return None

    def get_market_data_metadata(self) -> Optional[CacheMetadata]:
        """Get metadata for market data cache."""
        metadata_file = self.market_data_dir / "metadata.json"
        return self._load_metadata(metadata_file)

    # Results caching

    def save_results(
        self,
        results: Any,
        job_type: str,
        timestamp: Optional[datetime] = None
    ) -> Path:
        """
        Save screening results.

        Args:
            results: Results to save
            job_type: Type of job that produced results
            timestamp: Timestamp for results (default: now)

        Returns:
            Path to saved results file
        """
        if timestamp is None:
            timestamp = datetime.now()

        # Create filename with timestamp
        filename = f"{job_type}_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.results_dir / filename

        # Save results
        with open(filepath, 'w') as f:
            if hasattr(results, 'to_dict'):
                json.dump(results.to_dict(), f, indent=2)
            else:
                json.dump(results, f, indent=2, default=str)

        logger.info(f"Saved results to {filepath}")
        return filepath

    def load_latest_results(self, job_type: str) -> Optional[Any]:
        """
        Load most recent results for a job type.

        Args:
            job_type: Type of job

        Returns:
            Results or None if not found
        """
        # Find all result files for this job type
        pattern = f"{job_type}_*.json"
        result_files = sorted(self.results_dir.glob(pattern), reverse=True)

        if not result_files:
            logger.warning(f"No results found for job type: {job_type}")
            return None

        # Load most recent
        latest_file = result_files[0]
        try:
            with open(latest_file, 'r') as f:
                data = json.load(f)

            logger.info(f"Loaded results from {latest_file}")
            return data
        except Exception as e:
            logger.error(f"Failed to load results from {latest_file}: {e}")
            return None

    def cleanup_old_results(self, max_age_days: int = 30) -> int:
        """
        Remove old result files.

        Args:
            max_age_days: Maximum age in days

        Returns:
            Number of files deleted
        """
        cutoff = datetime.now() - timedelta(days=max_age_days)
        deleted_count = 0

        for result_file in self.results_dir.glob("*.json"):
            # Parse timestamp from filename
            try:
                # Extract timestamp part (format: YYYYMMDD_HHMMSS)
                timestamp_str = result_file.stem.split('_', 1)[1]
                file_time = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')

                if file_time < cutoff:
                    result_file.unlink()
                    deleted_count += 1
                    logger.debug(f"Deleted old result file: {result_file}")
            except Exception as e:
                logger.warning(f"Could not parse timestamp from {result_file}: {e}")

        logger.info(f"Cleaned up {deleted_count} old result files")
        return deleted_count

    # Helper methods

    def _load_metadata(self, metadata_file: Path) -> Optional[CacheMetadata]:
        """Load metadata from file."""
        if not metadata_file.exists():
            return None

        try:
            with open(metadata_file, 'r') as f:
                data = json.load(f)
            return CacheMetadata.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to load metadata from {metadata_file}: {e}")
            return None

    def get_cache_status(self) -> Dict[str, Any]:
        """
        Get status of all caches.

        Returns:
            Dictionary with cache status information
        """
        status = {
            'fundamentals': None,
            'market_data': None,
            'results_count': len(list(self.results_dir.glob("*.json")))
        }

        # Fundamentals status
        fund_metadata = self.get_fundamentals_metadata()
        if fund_metadata:
            status['fundamentals'] = {
                'updated_at': fund_metadata.updated_at.isoformat(),
                'record_count': fund_metadata.record_count,
                'age_hours': (datetime.now() - fund_metadata.updated_at).total_seconds() / 3600,
                'source': fund_metadata.data_source
            }

        # Market data status
        market_metadata = self.get_market_data_metadata()
        if market_metadata:
            status['market_data'] = {
                'updated_at': market_metadata.updated_at.isoformat(),
                'record_count': market_metadata.record_count,
                'age_minutes': (datetime.now() - market_metadata.updated_at).total_seconds() / 60,
                'source': market_metadata.data_source
            }

        return status

    def clear_cache(self, cache_type: Optional[str] = None) -> None:
        """
        Clear cache.

        Args:
            cache_type: Type of cache to clear ('fundamentals', 'market_data', 'results')
                       If None, clear all caches
        """
        if cache_type is None or cache_type == 'fundamentals':
            for file in self.fundamentals_dir.glob("*"):
                file.unlink()
            logger.info("Cleared fundamentals cache")

        if cache_type is None or cache_type == 'market_data':
            for file in self.market_data_dir.glob("*"):
                file.unlink()
            logger.info("Cleared market data cache")

        if cache_type is None or cache_type == 'results':
            for file in self.results_dir.glob("*"):
                file.unlink()
            logger.info("Cleared results cache")
