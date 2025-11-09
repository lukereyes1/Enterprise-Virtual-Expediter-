"""
Test Pydantic model validation and consistency.

Ensures that the central models validate correctly and JSON schemas
match the TypeScript type definitions.
"""

import pytest
from pydantic import ValidationError

from shortscreen.models import (
    MacroRegime,
    FactorScores,
    RawMetrics,
    MarketData,
    FundamentalData,
    ShortCandidate,
    JobStatus,
    JobType,
    JobPhaseMetrics,
    JobResult,
)


class TestMacroRegime:
    """Test MacroRegime model validation."""

    def test_valid_regime(self):
        """Test creating a valid macro regime."""
        regime = MacroRegime(downturn=0.8, inflation=0.6, liquidity=0.7)
        assert regime.downturn == 0.8
        assert regime.inflation == 0.6
        assert regime.liquidity == 0.7

    def test_regime_validation_too_high(self):
        """Test that values above 1.0 are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            MacroRegime(downturn=1.5, inflation=0.6, liquidity=0.7)
        assert "downturn" in str(exc_info.value)

    def test_regime_validation_negative(self):
        """Test that negative values are rejected."""
        with pytest.raises(ValidationError) as exc_info:
            MacroRegime(downturn=-0.1, inflation=0.6, liquidity=0.7)
        assert "downturn" in str(exc_info.value)

    def test_regime_json_roundtrip(self):
        """Test JSON serialization and deserialization."""
        regime = MacroRegime(downturn=0.8, inflation=0.6, liquidity=0.7)
        json_data = regime.model_dump_json()
        regime2 = MacroRegime.model_validate_json(json_data)
        assert regime == regime2


class TestFactorScores:
    """Test FactorScores model validation."""

    def test_valid_factor_scores(self):
        """Test creating valid factor scores."""
        scores = FactorScores(
            ticker="AAPL",
            valuation_score=85.3,
            profitability_score=12.4,
            growth_score=45.6,
            leverage_score=67.8,
            quality_score=23.1,
            market_score=78.9,
        )
        assert scores.ticker == "AAPL"
        assert 0 <= scores.valuation_score <= 100

    def test_factor_scores_out_of_range(self):
        """Test that scores above 100 are rejected."""
        with pytest.raises(ValidationError):
            FactorScores(
                ticker="AAPL",
                valuation_score=150.0,  # Invalid
                profitability_score=12.4,
                growth_score=45.6,
                leverage_score=67.8,
                quality_score=23.1,
                market_score=78.9,
            )

    def test_factor_scores_json_schema(self):
        """Test JSON schema generation."""
        schema = FactorScores.model_json_schema()
        assert schema["type"] == "object"
        assert "ticker" in schema["properties"]
        assert schema["properties"]["valuation_score"]["minimum"] == 0.0
        assert schema["properties"]["valuation_score"]["maximum"] == 100.0


class TestMarketData:
    """Test MarketData model validation."""

    def test_valid_market_data(self):
        """Test creating valid market data."""
        data = MarketData(
            ticker="AAPL",
            price=175.43,
            market_cap=2800000.0,
            beta=1.24,
            volume_20d_avg=52000000.0,
            price_52w_high=199.62,
            price_52w_low=124.17,
        )
        assert data.ticker == "AAPL"
        assert data.price > 0

    def test_market_data_negative_price(self):
        """Test that negative prices are rejected."""
        with pytest.raises(ValidationError):
            MarketData(
                ticker="AAPL",
                price=-10.0,  # Invalid
                market_cap=2800000.0,
                beta=1.24,
                volume_20d_avg=52000000.0,
                price_52w_high=199.62,
                price_52w_low=124.17,
            )


class TestShortCandidate:
    """Test ShortCandidate model validation."""

    def test_valid_short_candidate(self):
        """Test creating a valid short candidate."""
        candidate = ShortCandidate(
            ticker="TSLA",
            global_vulnerability_score=78.4,
            dominant_theme="Unprofitable Growth",
            dominant_theme_score=82.1,
            theme_scores={
                "Unprofitable Growth": 82.1,
                "High Beta Consumer": 75.8,
            },
            valuation_score=85.3,
            profitability_score=72.4,
            growth_score=45.6,
            leverage_score=67.8,
            quality_score=63.1,
            market_score=88.9,
            market_cap=800000.0,
            sector="Consumer Discretionary",
            revenue_growth=0.51,
            net_margin=0.03,
            debt_to_equity=0.87,
            beta=2.01,
        )
        assert candidate.ticker == "TSLA"
        assert candidate.dominant_theme == "Unprofitable Growth"


class TestJobModels:
    """Test Job-related models."""

    def test_job_status_enum(self):
        """Test JobStatus enum values."""
        assert JobStatus.SUCCESS == "success"
        assert JobStatus.FAILED == "failed"
        assert JobStatus.RUNNING == "running"

    def test_job_type_enum(self):
        """Test JobType enum values."""
        assert JobType.FULL_REFRESH == "full_refresh_daily"
        assert JobType.INCREMENTAL == "incremental_intraday"
        assert JobType.ON_DEMAND == "on_demand_scan"

    def test_valid_job_phase_metrics(self):
        """Test creating valid job phase metrics."""
        metrics = JobPhaseMetrics(
            phase_name="fetch_market_data",
            duration_seconds=12.5,
            records_processed=5000,
            success=True,
        )
        assert metrics.phase_name == "fetch_market_data"
        assert metrics.success is True

    def test_job_phase_metrics_negative_duration(self):
        """Test that negative duration is rejected."""
        with pytest.raises(ValidationError):
            JobPhaseMetrics(
                phase_name="fetch_market_data",
                duration_seconds=-1.0,  # Invalid
                records_processed=5000,
                success=True,
            )


class TestModelConsistency:
    """Test cross-model consistency."""

    def test_all_models_have_examples(self):
        """Verify all models have example data in schemas."""
        models_with_examples = [
            MacroRegime,
            FactorScores,
            RawMetrics,
            MarketData,
            FundamentalData,
            ShortCandidate,
            JobPhaseMetrics,
            JobResult,
        ]

        for model in models_with_examples:
            schema = model.model_json_schema()
            assert "examples" in schema, f"{model.__name__} missing examples"

    def test_all_models_have_descriptions(self):
        """Verify all models have descriptions."""
        models = [
            MacroRegime,
            FactorScores,
            RawMetrics,
            MarketData,
            FundamentalData,
            ShortCandidate,
            JobPhaseMetrics,
            JobResult,
        ]

        for model in models:
            schema = model.model_json_schema()
            assert "description" in schema, f"{model.__name__} missing description"

    def test_json_schema_generation(self):
        """Test that all models can generate JSON schemas."""
        models = [
            MacroRegime,
            FactorScores,
            RawMetrics,
            MarketData,
            FundamentalData,
            ShortCandidate,
            JobPhaseMetrics,
            JobResult,
        ]

        for model in models:
            schema = model.model_json_schema()
            assert "type" in schema
            assert "properties" in schema
            assert schema["type"] == "object"
