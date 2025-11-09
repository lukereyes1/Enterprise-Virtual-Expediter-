"""Configuration module for ShortScreen."""

import os
from pathlib import Path

CONFIG_DIR = Path(__file__).parent
THEME_CONFIG_PATH = CONFIG_DIR / "theme_config.yaml"
ETF_PROXIES_PATH = CONFIG_DIR / "etf_proxies.yaml"
