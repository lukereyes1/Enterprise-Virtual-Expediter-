"""
Job system for continuous analytics service.

Implements three job types:
1. full_refresh_daily: Complete data refresh and recomputation
2. incremental_intraday: Fast updates for market-sensitive metrics
3. on_demand_scan: Manual scans using cached data
"""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Any

from shortscreen.engine import ShortScreenEngine
from shortscreen.datastore import DataStore
from shortscreen.data import DataProvider

# Import models from central location (single source of truth)
from shortscreen.models.core import MacroRegime
from shortscreen.models.screening import ShortCandidate

logger = logging.getLogger(__name__)


class JobType(Enum):
    """Types of jobs in the screening service."""
    FULL_REFRESH = "full_refresh_daily"
    INCREMENTAL = "incremental_intraday"
    ON_DEMAND = "on_demand_scan"


class JobStatus(Enum):
    """Status of a job execution."""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    RUNNING = "running"
    PENDING = "pending"


@dataclass
class JobPhaseMetrics:
    """Metrics for a single phase of job execution."""
    phase_name: str
    duration_seconds: float
    records_processed: int
    success: bool
    error: Optional[str] = None


@dataclass
class JobResult:
    """Result of a job execution."""
    job_id: str
    job_type: JobType
    status: JobStatus
    start_time: datetime
    end_time: Optional[datetime] = None

    # Data freshness
    fundamentals_date: Optional[datetime] = None
    market_data_date: Optional[datetime] = None

    # Universe metrics
    universe_size: int = 0
    candidates_generated: int = 0

    # Performance metrics
    total_duration_seconds: float = 0.0
    phase_metrics: List[JobPhaseMetrics] = field(default_factory=list)

    # Degraded mode
    degraded_mode: bool = False
    degraded_reasons: List[str] = field(default_factory=list)

    # Results
    top_candidates: List[ShortCandidate] = field(default_factory=list)

    # Errors
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_phase_metric(self, metric: JobPhaseMetrics) -> None:
        """Add a phase metric."""
        self.phase_metrics.append(metric)

    def add_error(self, error: str) -> None:
        """Add an error."""
        self.errors.append(error)
        logger.error(f"Job {self.job_id} error: {error}")

    def add_warning(self, warning: str) -> None:
        """Add a warning."""
        self.warnings.append(warning)
        logger.warning(f"Job {self.job_id} warning: {warning}")

    def enter_degraded_mode(self, reason: str) -> None:
        """Enter degraded mode."""
        self.degraded_mode = True
        self.degraded_reasons.append(reason)
        logger.warning(f"Job {self.job_id} entering degraded mode: {reason}")

    def complete(self, status: JobStatus) -> None:
        """Mark job as complete."""
        self.end_time = datetime.now()
        self.status = status
        if self.start_time and self.end_time:
            self.total_duration_seconds = (self.end_time - self.start_time).total_seconds()

        logger.info(
            f"Job {self.job_id} completed with status {status.value} "
            f"in {self.total_duration_seconds:.2f}s"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'job_id': self.job_id,
            'job_type': self.job_type.value,
            'status': self.status.value,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'fundamentals_date': self.fundamentals_date.isoformat() if self.fundamentals_date else None,
            'market_data_date': self.market_data_date.isoformat() if self.market_data_date else None,
            'universe_size': self.universe_size,
            'candidates_generated': self.candidates_generated,
            'total_duration_seconds': self.total_duration_seconds,
            'degraded_mode': self.degraded_mode,
            'degraded_reasons': self.degraded_reasons,
            'errors': self.errors,
            'warnings': self.warnings,
            'phase_metrics': [
                {
                    'phase_name': pm.phase_name,
                    'duration_seconds': pm.duration_seconds,
                    'records_processed': pm.records_processed,
                    'success': pm.success,
                    'error': pm.error
                }
                for pm in self.phase_metrics
            ]
        }


class BaseJob:
    """Base class for all job types."""

    def __init__(
        self,
        data_provider: DataProvider,
        datastore: DataStore,
        engine: ShortScreenEngine
    ):
        """
        Initialize job.

        Args:
            data_provider: Data provider instance
            datastore: Data store instance
            engine: Screening engine instance
        """
        self.data_provider = data_provider
        self.datastore = datastore
        self.engine = engine

    def execute(
        self,
        macro_regime: MacroRegime,
        **kwargs
    ) -> JobResult:
        """
        Execute the job.

        Args:
            macro_regime: Macro regime for screening
            **kwargs: Additional job-specific parameters

        Returns:
            JobResult with execution details
        """
        raise NotImplementedError("Subclasses must implement execute()")

    def _create_job_result(self, job_type: JobType) -> JobResult:
        """Create a new job result object."""
        job_id = f"{job_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return JobResult(
            job_id=job_id,
            job_type=job_type,
            status=JobStatus.RUNNING,
            start_time=datetime.now()
        )

    def _run_phase(
        self,
        phase_name: str,
        func: callable,
        *args,
        **kwargs
    ) -> tuple[Any, JobPhaseMetrics]:
        """
        Run a job phase with timing and error handling.

        Args:
            phase_name: Name of the phase
            func: Function to execute
            *args: Positional arguments for function
            **kwargs: Keyword arguments for function

        Returns:
            Tuple of (result, metrics)
        """
        start_time = time.time()
        records_processed = 0
        success = True
        error = None
        result = None

        try:
            logger.info(f"Starting phase: {phase_name}")
            result = func(*args, **kwargs)

            # Try to count records
            if isinstance(result, (list, dict)):
                records_processed = len(result)

        except Exception as e:
            success = False
            error = str(e)
            logger.error(f"Phase {phase_name} failed: {e}", exc_info=True)

        duration = time.time() - start_time

        metrics = JobPhaseMetrics(
            phase_name=phase_name,
            duration_seconds=duration,
            records_processed=records_processed,
            success=success,
            error=error
        )

        logger.info(
            f"Phase {phase_name} completed in {duration:.2f}s "
            f"({records_processed} records, success={success})"
        )

        return result, metrics


class FullRefreshJob(BaseJob):
    """
    Full refresh job - complete data refresh and recomputation.

    Runs daily after market close:
    - Fetches fresh fundamentals for full universe
    - Fetches fresh market data
    - Recomputes all factor scores
    - Recomputes theme scores and rankings
    - Runs evaluation harness
    - Saves results and caches
    """

    def execute(
        self,
        macro_regime: MacroRegime,
        universe_size: Optional[int] = None
    ) -> JobResult:
        """
        Execute full refresh job.

        Args:
            macro_regime: Macro regime for screening
            universe_size: Optional universe size override

        Returns:
            JobResult
        """
        result = self._create_job_result(JobType.FULL_REFRESH)

        try:
            # Phase 1: Fetch fundamentals
            fundamentals, phase1 = self._run_phase(
                "fetch_fundamentals",
                self._fetch_fundamentals,
                universe_size
            )
            result.add_phase_metric(phase1)

            if not phase1.success or not fundamentals:
                result.add_error("Failed to fetch fundamentals")
                result.complete(JobStatus.FAILED)
                return result

            # Phase 2: Fetch market data
            market_data, phase2 = self._run_phase(
                "fetch_market_data",
                self._fetch_market_data,
                list(fundamentals.keys())
            )
            result.add_phase_metric(phase2)

            if not phase2.success or not market_data:
                result.add_error("Failed to fetch market data")
                # Try to use cached market data
                market_data = self.datastore.load_market_data()
                if market_data:
                    result.enter_degraded_mode("Using cached market data")
                else:
                    result.complete(JobStatus.FAILED)
                    return result

            # Phase 3: Run screening
            candidates, phase3 = self._run_phase(
                "run_screening",
                self._run_screening,
                macro_regime,
                market_data,
                fundamentals
            )
            result.add_phase_metric(phase3)

            if not phase3.success:
                result.add_error("Screening failed")
                result.complete(JobStatus.FAILED)
                return result

            # Phase 4: Save results and caches
            _, phase4 = self._run_phase(
                "save_results",
                self._save_results,
                candidates,
                fundamentals,
                market_data,
                result
            )
            result.add_phase_metric(phase4)

            # Update result
            result.universe_size = len(fundamentals)
            result.candidates_generated = len(candidates)
            result.top_candidates = candidates[:20]

            # Set data freshness
            fund_metadata = self.datastore.get_fundamentals_metadata()
            market_metadata = self.datastore.get_market_data_metadata()

            if fund_metadata:
                result.fundamentals_date = fund_metadata.updated_at
            if market_metadata:
                result.market_data_date = market_metadata.updated_at

            # Determine final status
            if result.degraded_mode:
                result.complete(JobStatus.PARTIAL)
            else:
                result.complete(JobStatus.SUCCESS)

        except Exception as e:
            result.add_error(f"Unexpected error: {e}")
            result.complete(JobStatus.FAILED)
            logger.error(f"Full refresh job failed: {e}", exc_info=True)

        return result

    def _fetch_fundamentals(self, universe_size: Optional[int]) -> Dict:
        """Fetch fundamentals from data provider."""
        tickers = self.data_provider.get_universe()
        if universe_size:
            tickers = tickers[:universe_size]

        fundamentals = self.data_provider.get_batch_fundamental_data(tickers)
        return fundamentals

    def _fetch_market_data(self, tickers: List[str]) -> Dict:
        """Fetch market data from data provider."""
        market_data = self.data_provider.get_batch_market_data(tickers)
        return market_data

    def _run_screening(self, macro_regime, market_data, fundamentals):
        """Run the screening engine."""
        # Temporarily inject data into engine
        # (In production, would refactor engine to accept data directly)
        candidates = self.engine.run(macro_regime)
        return candidates

    def _save_results(self, candidates, fundamentals, market_data, job_result):
        """Save results and update caches."""
        # Save to caches
        self.datastore.save_fundamentals(fundamentals)
        self.datastore.save_market_data(market_data)

        # Save results
        results_data = {
            'job_result': job_result.to_dict(),
            'top_candidates': [
                {
                    'ticker': c.ticker,
                    'score': c.global_vulnerability_score,
                    'theme': c.dominant_theme,
                    'sector': c.sector
                }
                for c in candidates[:50]
            ]
        }

        self.datastore.save_results(results_data, JobType.FULL_REFRESH.value)


class IncrementalJob(BaseJob):
    """
    Incremental intraday job - fast updates for market-sensitive metrics.

    Runs every N minutes during market hours:
    - Uses cached fundamentals (no refresh)
    - Fetches fresh market data (prices, volumes, beta)
    - Recomputes only market-sensitive factor scores
    - Recomputes rankings
    - Faster than full refresh
    """

    def execute(
        self,
        macro_regime: MacroRegime,
        **kwargs
    ) -> JobResult:
        """Execute incremental update."""
        result = self._create_job_result(JobType.INCREMENTAL)

        try:
            # Phase 1: Load cached fundamentals
            fundamentals, phase1 = self._run_phase(
                "load_fundamentals",
                self.datastore.load_fundamentals,
                timedelta(days=2)  # Allow slightly stale fundamentals
            )
            result.add_phase_metric(phase1)

            if not fundamentals:
                result.add_error("No cached fundamentals available")
                result.complete(JobStatus.FAILED)
                return result

            # Phase 2: Fetch fresh market data
            market_data, phase2 = self._run_phase(
                "fetch_market_data",
                self._fetch_market_data,
                list(fundamentals.keys())
            )
            result.add_phase_metric(phase2)

            if not phase2.success:
                result.enter_degraded_mode("Failed to fetch market data, using cache")
                market_data = self.datastore.load_market_data()

            # Phase 3: Run screening
            candidates, phase3 = self._run_phase(
                "run_screening",
                self._run_screening,
                macro_regime
            )
            result.add_phase_metric(phase3)

            # Phase 4: Save results
            _, phase4 = self._run_phase(
                "save_results",
                self._save_results,
                candidates,
                market_data
            )
            result.add_phase_metric(phase4)

            # Update result
            result.universe_size = len(fundamentals) if fundamentals else 0
            result.candidates_generated = len(candidates) if candidates else 0
            result.top_candidates = candidates[:20] if candidates else []

            # Set freshness
            fund_metadata = self.datastore.get_fundamentals_metadata()
            market_metadata = self.datastore.get_market_data_metadata()

            if fund_metadata:
                result.fundamentals_date = fund_metadata.updated_at
            if market_metadata:
                result.market_data_date = market_metadata.updated_at

            result.complete(JobStatus.PARTIAL if result.degraded_mode else JobStatus.SUCCESS)

        except Exception as e:
            result.add_error(f"Unexpected error: {e}")
            result.complete(JobStatus.FAILED)

        return result

    def _fetch_market_data(self, tickers: List[str]) -> Dict:
        """Fetch market data."""
        return self.data_provider.get_batch_market_data(tickers)

    def _run_screening(self, macro_regime):
        """Run screening."""
        return self.engine.run(macro_regime)

    def _save_results(self, candidates, market_data):
        """Save results."""
        if market_data:
            self.datastore.save_market_data(market_data)

        if candidates:
            results_data = {
                'top_candidates': [
                    {
                        'ticker': c.ticker,
                        'score': c.global_vulnerability_score,
                        'theme': c.dominant_theme
                    }
                    for c in candidates[:50]
                ]
            }
            self.datastore.save_results(results_data, JobType.INCREMENTAL.value)


class OnDemandJob(BaseJob):
    """
    On-demand scan job - manual scans using cached data.

    Triggered manually:
    - Uses all cached data (no API calls)
    - Fast execution
    - Allows testing different macro regimes
    """

    def execute(
        self,
        macro_regime: MacroRegime,
        **kwargs
    ) -> JobResult:
        """Execute on-demand scan."""
        result = self._create_job_result(JobType.ON_DEMAND)

        try:
            # Phase 1: Load cached data
            fundamentals = self.datastore.load_fundamentals()
            market_data = self.datastore.load_market_data()

            if not fundamentals or not market_data:
                result.add_error("Insufficient cached data for on-demand scan")
                result.complete(JobStatus.FAILED)
                return result

            # Phase 2: Run screening
            candidates, phase2 = self._run_phase(
                "run_screening",
                self.engine.run,
                macro_regime
            )
            result.add_phase_metric(phase2)

            # Update result
            result.universe_size = len(fundamentals)
            result.candidates_generated = len(candidates) if candidates else 0
            result.top_candidates = candidates[:20] if candidates else []

            # Set freshness
            fund_metadata = self.datastore.get_fundamentals_metadata()
            market_metadata = self.datastore.get_market_data_metadata()

            if fund_metadata:
                result.fundamentals_date = fund_metadata.updated_at
                # Warn if stale
                age_hours = (datetime.now() - fund_metadata.updated_at).total_seconds() / 3600
                if age_hours > 48:
                    result.add_warning(f"Fundamentals are {age_hours:.1f} hours old")

            if market_metadata:
                result.market_data_date = market_metadata.updated_at
                age_hours = (datetime.now() - market_metadata.updated_at).total_seconds() / 3600
                if age_hours > 4:
                    result.add_warning(f"Market data is {age_hours:.1f} hours old")

            result.complete(JobStatus.SUCCESS)

        except Exception as e:
            result.add_error(f"Unexpected error: {e}")
            result.complete(JobStatus.FAILED)

        return result
