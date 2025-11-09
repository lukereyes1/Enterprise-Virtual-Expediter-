"""
Data models for market and fundamental data.

These models represent raw data from external data providers.
"""

from pydantic import BaseModel, Field


class MarketData(BaseModel):
    """Market data for a ticker."""
    ticker: str = Field(description="Stock ticker symbol")
    price: float = Field(gt=0, description="Current stock price")
    market_cap: float = Field(gt=0, description="Market capitalization in millions")
    beta: float = Field(description="Market beta")
    volume_20d_avg: float = Field(gt=0, description="20-day average volume")
    price_52w_high: float = Field(gt=0, description="52-week high price")
    price_52w_low: float = Field(gt=0, description="52-week low price")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "AAPL",
                    "price": 175.43,
                    "market_cap": 2800000.0,
                    "beta": 1.24,
                    "volume_20d_avg": 52000000.0,
                    "price_52w_high": 199.62,
                    "price_52w_low": 124.17
                }
            ]
        }
    }


class FundamentalData(BaseModel):
    """Fundamental data for a ticker."""
    ticker: str = Field(description="Stock ticker symbol")

    # Income statement
    revenue: float = Field(description="Total revenue in millions")
    revenue_growth: float = Field(description="Year-over-year revenue growth rate")
    ebitda: float = Field(description="EBITDA in millions")
    net_income: float = Field(description="Net income in millions")
    free_cash_flow: float = Field(description="Free cash flow in millions")

    # Balance sheet
    total_debt: float = Field(ge=0, description="Total debt in millions")
    cash: float = Field(ge=0, description="Cash and equivalents in millions")
    total_assets: float = Field(gt=0, description="Total assets in millions")
    total_equity: float = Field(description="Total equity in millions")

    # Share information
    shares_outstanding: float = Field(gt=0, description="Shares outstanding in millions")

    # Classification
    sector: str = Field(description="Sector classification")
    industry: str = Field(description="Industry classification")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ticker": "AAPL",
                    "revenue": 383285.0,
                    "revenue_growth": 0.08,
                    "ebitda": 114301.0,
                    "net_income": 96995.0,
                    "free_cash_flow": 99584.0,
                    "total_debt": 111088.0,
                    "cash": 61555.0,
                    "total_assets": 352755.0,
                    "total_equity": 62146.0,
                    "shares_outstanding": 15552.8,
                    "sector": "Technology",
                    "industry": "Consumer Electronics"
                }
            ]
        }
    }
