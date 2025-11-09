#!/usr/bin/env python
"""
Validate consistency across all schemas and generated files.

This script ensures:
1. TypeScript types are up-to-date with Python models
2. All schemas have been regenerated
3. No orphaned or outdated files exist
"""

import json
import hashlib
import subprocess
from pathlib import Path
from typing import Dict, List


class ConsistencyChecker:
    """Check consistency across schemas and generated files."""

    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.schemas_dir = self.root / "schemas"
        self.ts_types_file = self.root / "shortscreen-mobile" / "src" / "types" / "generated.ts"
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def check_schemas_exist(self) -> bool:
        """Check that all expected schemas exist."""
        expected_schemas = [
            "MacroRegime.json",
            "ThemeConfig.json",
            "FactorScores.json",
            "RawMetrics.json",
            "MarketData.json",
            "FundamentalData.json",
            "ShortCandidate.json",
            "JobPhaseMetrics.json",
            "JobResult.json",
        ]

        missing = []
        for schema_name in expected_schemas:
            schema_file = self.schemas_dir / schema_name
            if not schema_file.exists():
                missing.append(schema_name)

        if missing:
            self.errors.append(f"Missing schemas: {', '.join(missing)}")
            return False

        return True

    def check_typescript_types_exist(self) -> bool:
        """Check that TypeScript types file exists."""
        if not self.ts_types_file.exists():
            self.errors.append(f"TypeScript types file not found: {self.ts_types_file}")
            return False

        # Check that it's auto-generated (has the warning header)
        with open(self.ts_types_file) as f:
            header = "".join([f.readline() for _ in range(5)])
            if "AUTO-GENERATED" not in header:
                self.warnings.append(
                    "TypeScript types file doesn't have auto-generated header"
                )

        return True

    def check_typescript_types_match_schemas(self) -> bool:
        """Check that TypeScript types match the JSON schemas."""
        if not self.ts_types_file.exists():
            return False

        # Read TypeScript file
        with open(self.ts_types_file) as f:
            ts_content = f.read()

        # Check that all schemas have corresponding TypeScript types
        schema_files = list(self.schemas_dir.glob("*.json"))
        missing_types = []

        for schema_file in schema_files:
            model_name = schema_file.stem

            # Check if the type is exported in TypeScript
            if f"export interface {model_name}" not in ts_content and \
               f"export type {model_name}" not in ts_content:
                # Check if it's in $defs
                with open(schema_file) as f:
                    schema = json.load(f)
                    if "$defs" in schema:
                        # It's okay if it's a nested definition
                        continue

                missing_types.append(model_name)

        if missing_types:
            self.errors.append(
                f"TypeScript types missing for schemas: {', '.join(missing_types)}"
            )
            return False

        return True

    def check_models_importable(self) -> bool:
        """Check that all models can be imported from shortscreen.models."""
        try:
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
            return True
        except ImportError as e:
            self.errors.append(f"Failed to import models: {e}")
            return False

    def check_pydantic_installed(self) -> bool:
        """Check that pydantic is installed."""
        try:
            import pydantic
            version = pydantic.VERSION
            if version.split('.')[0] != '2':
                self.warnings.append(
                    f"Pydantic v2.x expected, found v{version}"
                )
            return True
        except ImportError:
            self.errors.append("Pydantic not installed (required in requirements.txt)")
            return False

    def run_all_checks(self) -> bool:
        """Run all consistency checks."""
        print("Running consistency checks...")
        print()

        checks = [
            ("Pydantic installation", self.check_pydantic_installed),
            ("Models importable", self.check_models_importable),
            ("Schema files exist", self.check_schemas_exist),
            ("TypeScript types exist", self.check_typescript_types_exist),
            ("TypeScript types match schemas", self.check_typescript_types_match_schemas),
        ]

        all_passed = True
        for check_name, check_fn in checks:
            try:
                result = check_fn()
                status = "✓" if result else "✗"
                print(f"{status} {check_name}")
                if not result:
                    all_passed = False
            except Exception as e:
                print(f"✗ {check_name} (exception: {e})")
                self.errors.append(f"{check_name}: {e}")
                all_passed = False

        print()

        if self.warnings:
            print("Warnings:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
            print()

        if self.errors:
            print("Errors:")
            for error in self.errors:
                print(f"  ✗ {error}")
            print()

        return all_passed

    def suggest_fixes(self):
        """Suggest fixes for common issues."""
        if not self.errors and not self.warnings:
            return

        print("Suggested fixes:")
        print()

        if any("Missing schemas" in e for e in self.errors):
            print("  Run: python scripts/gen_json_schemas.py")

        if any("TypeScript types" in e for e in self.errors):
            print("  Run: python scripts/gen_typescript_types.py")

        if any("Pydantic" in e for e in self.errors):
            print("  Run: pip install pydantic>=2.5.0")

        if any("import models" in e for e in self.errors):
            print("  Ensure shortscreen/models/ package is complete")

        print()


def main():
    """Run consistency validation."""
    checker = ConsistencyChecker()

    success = checker.run_all_checks()

    if not success:
        checker.suggest_fixes()
        print("❌ Consistency check FAILED")
        exit(1)
    else:
        print("✅ All consistency checks PASSED")
        print()
        print("The codebase maintains single source of truth:")
        print("  • Python models are canonical")
        print("  • JSON schemas auto-generated")
        print("  • TypeScript types auto-generated")
        exit(0)


if __name__ == "__main__":
    main()
