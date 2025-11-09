# ShortScreen

A systematic macro-to-theme-to-target engine for identifying bearish investment opportunities.

## Overview

ShortScreen implements a quantitative framework for short selling that connects:
1. **Macro Regime** - Economic indicators (downturn, inflation, liquidity stress)
2. **Investment Themes** - Four thematic vulnerabilities
3. **Stock Selection** - Percentile-based factor scoring

## Features

- **Config-Driven**: All weights, sensitivities, and thresholds in YAML
- **Modular Design**: Clean separation of data, factors, themes, and orchestration
- **Type-Safe**: Full type hints and dataclasses throughout
- **Testable**: Mock data provider for unit testing
- **Extensible**: Easy to add new themes, factors, or data sources

## Installation

```bash
pip install -e .
```

Or for development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```bash
# Run with baseline macro regime
shortscreen-cli --downturn 0.5 --inflation 0.5 --liquidity 0.5

# Run with high stress regime
shortscreen-cli --downturn 0.9 --inflation 0.8 --liquidity 0.8

# Show only top 10 candidates
shortscreen-cli --downturn 0.7 --inflation 0.6 --liquidity 0.5 --top 10
```

## Architecture

### Core Modules

- **`data.py`**: Data abstraction layer with mock and real API support
- **`factors.py`**: Raw metrics and percentile-based factor scoring
- **`themes.py`**: Four investment themes with filtering and scoring logic
- **`macro.py`**: Macro regime indicators and theme weight computation
- **`engine.py`**: Main orchestration engine
- **`cli.py`**: Command-line interface

### Investment Themes

1. **Unprofitable Growth**
   - Targets: High-growth, unprofitable companies
   - Vulnerabilities: Valuation compression, profitability concerns
   - ETF Proxies: ARKK, ARKW, XLK

2. **Over-Leveraged Small Caps**
   - Targets: Small-cap companies with high debt
   - Vulnerabilities: Refinancing risk, liquidity stress
   - ETF Proxies: IWM, SLY, IJR

3. **High Beta Consumer**
   - Targets: Consumer discretionary with high market sensitivity
   - Vulnerabilities: Economic downturn, spending slowdown
   - ETF Proxies: XLY, XRT, FXD

4. **Weak Financials**
   - Targets: Financial companies with weak fundamentals
   - Vulnerabilities: Credit deterioration, capital concerns
   - ETF Proxies: XLF, KRE, IAI

### Factor Scores

All scores are percentile-based (0-100), where higher = more bearish:

- **Valuation**: P/S, P/B, EV/EBITDA
- **Profitability**: Net margin, EBITDA margin, ROE
- **Growth**: Revenue growth trajectory
- **Leverage**: Debt/Equity, Debt/Assets, Net Debt/EBITDA
- **Quality**: FCF margin, current ratio
- **Market**: Beta, distance from 52-week high

## Configuration

### Theme Configuration (`shortscreen/config/theme_config.yaml`)

Defines base weights and macro sensitivities for each theme.

### ETF Proxies (`shortscreen/config/etf_proxies.yaml`)

Maps themes to representative ETF tickers.

## Python API

```python
from shortscreen import ShortScreenEngine
from shortscreen.macro import MacroRegime

# Create engine
engine = ShortScreenEngine()

# Define macro regime
regime = MacroRegime(
    downturn=0.8,
    inflation=0.7,
    liquidity=0.6
)

# Run screening
candidates = engine.run(regime)

# Get top candidates
for candidate in candidates[:10]:
    print(f"{candidate.ticker}: {candidate.global_vulnerability_score:.1f}")
    print(f"  Theme: {candidate.dominant_theme}")
    print(f"  Sector: {candidate.sector}")
```

## Development

### Running Tests

```bash
pytest tests/ -v --cov=shortscreen
```

### Type Checking

```bash
mypy shortscreen/
```

### Code Formatting

```bash
black shortscreen/ tests/
flake8 shortscreen/ tests/
```
