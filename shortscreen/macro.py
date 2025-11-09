"""
Macro regime module for computing theme weights.

This module defines macro regime indicators and logic to compute
theme-specific weights based on current macro conditions.
"""

from typing import Dict
import yaml

from shortscreen.config import THEME_CONFIG_PATH

# Import models from central location (single source of truth)
from shortscreen.models.core import MacroRegime, ThemeConfig


def load_theme_config() -> Dict[str, ThemeConfig]:
    """
    Load theme configuration from YAML file.

    Returns:
        Dictionary mapping theme names to ThemeConfig objects
    """
    try:
        with open(THEME_CONFIG_PATH, 'r') as f:
            config = yaml.safe_load(f)
            themes_config = config.get('themes', {})

            result = {}
            for theme_key, theme_data in themes_config.items():
                result[theme_key] = ThemeConfig(
                    base_weight=theme_data['base_weight'],
                    sensitivities=theme_data['sensitivities']
                )
            return result
    except Exception as e:
        raise RuntimeError(f"Failed to load theme config: {e}")


def compute_theme_weights(macro_regime: MacroRegime) -> Dict[str, float]:
    """
    Compute theme-specific weights based on macro regime.

    The weight for each theme is computed as:
        weight = base_weight * (1 + Σ(sensitivity_i * regime_i))

    Where:
    - base_weight: baseline weight for the theme
    - sensitivity_i: theme's sensitivity to macro factor i
    - regime_i: current value of macro factor i (0-1)

    Weights are then normalized to sum to 1.0.

    Args:
        macro_regime: Current macro regime indicators

    Returns:
        Dictionary mapping theme keys to normalized weights
    """
    theme_configs = load_theme_config()

    # Compute raw weights
    raw_weights = {}
    for theme_key, config in theme_configs.items():
        # Calculate macro adjustment
        macro_adjustment = (
            config.sensitivities['downturn'] * macro_regime.downturn +
            config.sensitivities['inflation'] * macro_regime.inflation +
            config.sensitivities['liquidity'] * macro_regime.liquidity
        )

        # Compute weighted score
        raw_weight = config.base_weight * (1.0 + macro_adjustment)
        raw_weights[theme_key] = max(raw_weight, 0.0)  # Ensure non-negative

    # Normalize weights to sum to 1.0
    total_weight = sum(raw_weights.values())
    if total_weight == 0:
        # Fallback to equal weights if all are zero
        normalized_weights = {key: 1.0 / len(raw_weights) for key in raw_weights}
    else:
        normalized_weights = {key: w / total_weight for key, w in raw_weights.items()}

    return normalized_weights


def get_theme_name_mapping() -> Dict[str, str]:
    """
    Map theme config keys to display names.

    Returns:
        Dictionary mapping config keys to display names
    """
    return {
        'unprofitable_growth': 'Unprofitable Growth',
        'overleveraged_smallcaps': 'Over-Leveraged Small Caps',
        'highbeta_consumer': 'High Beta Consumer',
        'weak_financials': 'Weak Financials'
    }
