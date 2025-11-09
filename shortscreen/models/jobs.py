"""
Job models for continuous analytics service.

Models for job execution, status tracking, and metrics.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from shortscreen.models.screening import ShortCandidate


class JobType(str, Enum):
    """Types of jobs in the screening service."""
    FULL_REFRESH = "full_refresh_daily"
    INCREMENTAL = "incremental_intraday"
    ON_DEMAND = "on_demand_scan"


class JobStatus(str, Enum):
    """Status of a job execution."""
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    RUNNING = "running"
    PENDING = "pending"


class JobPhaseMetrics(BaseModel):
    """Metrics for a single phase of job execution."""
    phase_name: str = Field(description="Name of the execution phase")
    duration_seconds: float = Field(ge=0, description="Duration of the phase in seconds")
    records_processed: int = Field(ge=0, description="Number of records processed")
    success: bool = Field(description="Whether the phase succeeded")
    error: Optional[str] = Field(default=None, description="Error message if phase failed")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "phase_name": "fetch_market_data",
                    "duration_seconds": 12.5,
                    "records_processed": 5000,
                    "success": True,
                    "error": None
                }
            ]
        }
    }


class JobResult(BaseModel):
    """Result of a job execution."""
    job_id: str = Field(description="Unique job identifier")
    job_type: JobType = Field(description="Type of job")
    status: JobStatus = Field(description="Job execution status")
    start_time: datetime = Field(description="Job start timestamp")
    end_time: Optional[datetime] = Field(default=None, description="Job end timestamp")

    # Data freshness
    fundamentals_date: Optional[datetime] = Field(
        default=None,
        description="Timestamp of fundamental data"
    )
    market_data_date: Optional[datetime] = Field(
        default=None,
        description="Timestamp of market data"
    )

    # Universe metrics
    universe_size: int = Field(default=0, ge=0, description="Total universe size")
    candidates_generated: int = Field(default=0, ge=0, description="Number of candidates generated")

    # Performance metrics
    total_duration_seconds: float = Field(default=0.0, ge=0, description="Total job duration")
    phase_metrics: List[JobPhaseMetrics] = Field(
        default_factory=list,
        description="Metrics for each execution phase"
    )

    # Degraded mode
    degraded_mode: bool = Field(default=False, description="Whether job ran in degraded mode")
    degraded_reasons: List[str] = Field(
        default_factory=list,
        description="Reasons for degraded mode"
    )

    # Results
    top_candidates: List[ShortCandidate] = Field(
        default_factory=list,
        description="Top short candidates from screening"
    )

    # Errors and warnings
    errors: List[str] = Field(default_factory=list, description="Error messages")
    warnings: List[str] = Field(default_factory=list, description="Warning messages")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for serialization.

        Returns:
            Dictionary representation of the job result
        """
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
            'phase_metrics': [pm.model_dump() for pm in self.phase_metrics],
            'top_candidates': [c.model_dump() for c in self.top_candidates]
        }

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "job_id": "job_20250109_093000",
                    "job_type": "full_refresh_daily",
                    "status": "success",
                    "start_time": "2025-01-09T09:30:00Z",
                    "end_time": "2025-01-09T09:35:23Z",
                    "fundamentals_date": "2025-01-09T08:00:00Z",
                    "market_data_date": "2025-01-09T09:29:00Z",
                    "universe_size": 5000,
                    "candidates_generated": 500,
                    "total_duration_seconds": 323.5,
                    "degraded_mode": False,
                    "degraded_reasons": [],
                    "errors": [],
                    "warnings": [],
                    "phase_metrics": [],
                    "top_candidates": []
                }
            ]
        }
    }
