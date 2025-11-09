#!/usr/bin/env python
"""
Generate TypeScript types from Pydantic models.

This script reads JSON schemas generated from Pydantic models and converts
them to TypeScript interfaces and types. This ensures TypeScript types
always match Python models (single source of truth).
"""

import json
from pathlib import Path
from typing import Dict, Any, List


def json_type_to_ts_type(json_type: str, format_hint: str = None) -> str:
    """
    Convert JSON schema type to TypeScript type.

    Args:
        json_type: JSON schema type (string, number, etc.)
        format_hint: Optional format hint (date-time, etc.)

    Returns:
        TypeScript type string
    """
    if format_hint == "date-time":
        return "string"  # ISO date strings in JSON

    type_mapping = {
        "string": "string",
        "number": "number",
        "integer": "number",
        "boolean": "boolean",
        "array": "Array",
        "object": "Record<string, any>",
        "null": "null",
    }
    return type_mapping.get(json_type, "any")


def property_to_ts_type(prop_schema: Dict[str, Any]) -> str:
    """
    Convert a JSON schema property to TypeScript type.

    Args:
        prop_schema: Property schema from JSON schema

    Returns:
        TypeScript type string
    """
    # Handle enums
    if "enum" in prop_schema:
        enum_values = [f'"{v}"' for v in prop_schema["enum"]]
        return " | ".join(enum_values)

    # Handle arrays
    if prop_schema.get("type") == "array":
        if "items" in prop_schema:
            item_type = property_to_ts_type(prop_schema["items"])
            return f"Array<{item_type}>"
        return "Array<any>"

    # Handle objects/records
    if prop_schema.get("type") == "object":
        # Check if it's a Record type
        if "additionalProperties" in prop_schema:
            value_type = property_to_ts_type(prop_schema["additionalProperties"])
            return f"Record<string, {value_type}>"
        return "Record<string, any>"

    # Handle refs (nested models)
    if "$ref" in prop_schema:
        ref = prop_schema["$ref"]
        # Extract model name from ref like "#/$defs/ShortCandidate"
        model_name = ref.split("/")[-1]
        return model_name

    # Handle anyOf (union types)
    if "anyOf" in prop_schema:
        types = [property_to_ts_type(t) for t in prop_schema["anyOf"]]
        return " | ".join(types)

    # Basic types
    json_type = prop_schema.get("type", "any")
    format_hint = prop_schema.get("format")
    return json_type_to_ts_type(json_type, format_hint)


def generate_ts_interface(schema: Dict[str, Any], name: str) -> str:
    """
    Generate TypeScript interface from JSON schema.

    Args:
        schema: JSON schema dictionary
        name: Interface name

    Returns:
        TypeScript interface definition
    """
    lines = []

    # Add description as JSDoc comment
    if "description" in schema:
        lines.append("/**")
        lines.append(f" * {schema['description']}")
        lines.append(" */")

    # Start interface
    lines.append(f"export interface {name} {{")

    # Add properties
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))

    for prop_name, prop_schema in properties.items():
        # Add property description
        if "description" in prop_schema:
            lines.append(f"  /** {prop_schema['description']} */")

        # Determine if optional
        optional = "?" if prop_name not in required else ""

        # Get TypeScript type
        ts_type = property_to_ts_type(prop_schema)

        lines.append(f"  {prop_name}{optional}: {ts_type};")

    lines.append("}")

    return "\n".join(lines)


def generate_ts_enum(schema: Dict[str, Any], name: str) -> str:
    """
    Generate TypeScript enum or type alias.

    Args:
        schema: JSON schema dictionary
        name: Enum name

    Returns:
        TypeScript enum or type definition
    """
    # Check if this is an enum
    if "enum" in schema:
        values = schema["enum"]
        lines = []

        # Add description as JSDoc comment
        if "description" in schema:
            lines.append("/**")
            lines.append(f" * {schema['description']}")
            lines.append(" */")

        # Generate type alias with union of literals
        type_values = " | ".join([f'"{v}"' for v in values])
        lines.append(f"export type {name} = {type_values};")

        return "\n".join(lines)

    return ""


def generate_ts_file(schema_files: List[Path], output_file: Path) -> None:
    """
    Generate TypeScript types file from JSON schemas.

    Args:
        schema_files: List of JSON schema files
        output_file: Output TypeScript file path
    """
    lines = [
        "/**",
        " * AUTO-GENERATED TypeScript types from Python Pydantic models",
        " * DO NOT EDIT MANUALLY - Run scripts/gen_typescript_types.py to regenerate",
        " */",
        "",
    ]

    # Collect all definitions from $defs
    all_defs = {}

    # First pass: collect all $defs
    for schema_file in sorted(schema_files):
        with open(schema_file) as f:
            schema = json.load(f)

        # Extract $defs if present
        if "$defs" in schema:
            for def_name, def_schema in schema["$defs"].items():
                if def_name not in all_defs:
                    all_defs[def_name] = def_schema

    # Generate types for $defs first (enums, nested types)
    for def_name, def_schema in sorted(all_defs.items()):
        if "enum" in def_schema:
            ts_code = generate_ts_enum(def_schema, def_name)
        else:
            ts_code = generate_ts_interface(def_schema, def_name)

        if ts_code:
            lines.append("")
            lines.append(ts_code)

    # Second pass: process main schemas
    for schema_file in sorted(schema_files):
        with open(schema_file) as f:
            schema = json.load(f)

        model_name = schema_file.stem

        # Skip if already generated from $defs
        if model_name in all_defs:
            continue

        # Generate interface or enum
        if "enum" in schema:
            ts_code = generate_ts_enum(schema, model_name)
        else:
            ts_code = generate_ts_interface(schema, model_name)

        if ts_code:
            lines.append("")
            lines.append(ts_code)

    # Write output file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write("\n".join(lines))
        f.write("\n")

    print(f"✓ Generated TypeScript types: {output_file}")


def main():
    """Generate TypeScript types from JSON schemas."""
    # Get schema directory
    schemas_dir = Path(__file__).parent.parent / "schemas"
    if not schemas_dir.exists():
        print("ERROR: schemas/ directory not found")
        print("Run scripts/gen_json_schemas.py first to generate JSON schemas")
        return

    # Get all schema files
    schema_files = list(schemas_dir.glob("*.json"))
    if not schema_files:
        print("ERROR: No schema files found in schemas/")
        return

    print("Generating TypeScript types from JSON schemas...")
    print()

    # Generate types for mobile app
    mobile_types_file = Path(__file__).parent.parent / "shortscreen-mobile" / "src" / "types" / "generated.ts"
    generate_ts_file(schema_files, mobile_types_file)

    print()
    print(f"✓ Generated TypeScript types from {len(schema_files)} schemas")
    print()
    print("Usage in TypeScript:")
    print("  import { FactorScores, ShortCandidate } from './types/generated';")


if __name__ == "__main__":
    main()
