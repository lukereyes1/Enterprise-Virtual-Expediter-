#!/usr/bin/env python
"""
Generate JSON schemas from Pydantic models.

This script generates JSON schemas for all Pydantic models in the
shortscreen.models package. These schemas can be used for:
- API documentation
- TypeScript type generation
- Validation in other languages
- Configuration file validation
"""

import json
from pathlib import Path
from typing import Type
from pydantic import BaseModel

from shortscreen.models import (
    MacroRegime,
    ThemeConfig,
    FactorScores,
    RawMetrics,
    MarketData,
    FundamentalData,
    ShortCandidate,
    JobType,
    JobStatus,
    JobPhaseMetrics,
    JobResult,
    ReportMetadata,
    RiskIndicators,
    SectorDistribution,
    ThemeDistribution,
    FactorDistribution,
    NarrativeSummary,
    ScreeningReport,
)


def generate_schema(model: Type[BaseModel], output_dir: Path) -> None:
    """
    Generate JSON schema for a Pydantic model.

    Args:
        model: Pydantic model class
        output_dir: Directory to write schema file
    """
    schema = model.model_json_schema()
    schema_file = output_dir / f"{model.__name__}.json"

    with open(schema_file, 'w') as f:
        json.dump(schema, f, indent=2)

    print(f"✓ Generated schema: {schema_file}")


def main():
    """Generate all JSON schemas."""
    # Create output directory
    output_dir = Path(__file__).parent.parent / "schemas"
    output_dir.mkdir(exist_ok=True)

    print("Generating JSON schemas...")
    print()

    # Generate schemas for all models
    models = [
        MacroRegime,
        ThemeConfig,
        FactorScores,
        RawMetrics,
        MarketData,
        FundamentalData,
        ShortCandidate,
        JobPhaseMetrics,
        JobResult,
        ReportMetadata,
        RiskIndicators,
        SectorDistribution,
        ThemeDistribution,
        FactorDistribution,
        NarrativeSummary,
        ScreeningReport,
    ]

    for model in models:
        generate_schema(model, output_dir)

    print()
    print(f"✓ Generated {len(models)} JSON schemas in {output_dir}")
    print()
    print("These schemas can be used for:")
    print("  - TypeScript type generation")
    print("  - API documentation")
    print("  - Configuration validation")
    print("  - Cross-language validation")


if __name__ == "__main__":
    main()
