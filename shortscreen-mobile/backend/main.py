"""
FastAPI backend stub for ShortScreen Command mobile app
Serves mock data matching the API specification
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import random

app = FastAPI(title="ShortScreen API", version="1.0.0")

# CORS middleware for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify mobile app origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models

class RegimeStatus(BaseModel):
    status: str
    risk_off_score: float
    small_cap_stress_score: float
    avg_beta: float

class ThemeSummary(BaseModel):
    name: str
    display_name: str
    score: float
    trend: str
    top_decile_count: int
    score_change_24h: float

class DataFreshness(BaseModel):
    fundamentals_updated_at: datetime
    market_data_updated_at: datetime

class StatusResponse(BaseModel):
    timestamp: datetime
    regime: RegimeStatus
    themes: List[ThemeSummary]
    data_freshness: DataFreshness

class Event(BaseModel):
    id: str
    type: str
    title: str
    body: str
    created_at: datetime
    read: bool
    priority: str
    data: dict

class EventsResponse(BaseModel):
    events: List[Event]
    pagination: dict

class FactorScores(BaseModel):
    leverage: float
    valuation: float
    beta: float
    quality: float
    growth: float
    duration: float

class TickerDetail(BaseModel):
    ticker: str
    company_name: str
    sector: str
    market_cap: float
    global_score: float
    in_top_decile: bool
    factor_scores: FactorScores
    theme_scores: dict
    primary_theme: str
    days_in_top_decile: int

# Mock Data Generators

def generate_mock_status() -> StatusResponse:
    """Generate mock status data"""
    return StatusResponse(
        timestamp=datetime.now(),
        regime=RegimeStatus(
            status=random.choice(["risk_off", "neutral", "risk_on"]),
            risk_off_score=random.uniform(0.5, 0.9),
            small_cap_stress_score=random.uniform(0.4, 0.8),
            avg_beta=random.uniform(1.2, 1.6)
        ),
        themes=[
            ThemeSummary(
                name="unprofitable_growth",
                display_name="Unprofitable Growth",
                score=random.uniform(60, 85),
                trend=random.choice(["up", "down", "flat"]),
                top_decile_count=random.randint(15, 30),
                score_change_24h=random.uniform(-5, 10)
            ),
            ThemeSummary(
                name="overleveraged_smallcaps",
                display_name="Over-Leveraged Small Caps",
                score=random.uniform(55, 80),
                trend=random.choice(["up", "down", "flat"]),
                top_decile_count=random.randint(12, 25),
                score_change_24h=random.uniform(-5, 10)
            ),
            ThemeSummary(
                name="highbeta_consumer",
                display_name="High Beta Consumer",
                score=random.uniform(65, 90),
                trend=random.choice(["up", "down", "flat"]),
                top_decile_count=random.randint(18, 35),
                score_change_24h=random.uniform(-5, 10)
            ),
            ThemeSummary(
                name="weak_financials",
                display_name="Weak Financials",
                score=random.uniform(50, 75),
                trend=random.choice(["up", "down", "flat"]),
                top_decile_count=random.randint(10, 22),
                score_change_24h=random.uniform(-5, 10)
            ),
        ],
        data_freshness=DataFreshness(
            fundamentals_updated_at=datetime.now() - timedelta(hours=8),
            market_data_updated_at=datetime.now() - timedelta(minutes=2)
        )
    )

def generate_mock_events() -> List[Event]:
    """Generate mock events"""
    events = []
    event_types = [
        ("regime_change", "Risk regime changed", "Neutral → Risk-Off", "high"),
        ("theme_spike", "Unprofitable Growth", "+5 new top decile names", "medium"),
        ("ticker_alert", "TSLA entered top decile", "Global score: 78.4", "medium"),
        ("theme_spike", "High Beta Consumer", "Score spike 65 → 78", "medium"),
        ("system_alert", "Data provider unavailable", "Running in cache-only mode", "high"),
    ]

    for i, (event_type, title, body, priority) in enumerate(event_types):
        events.append(Event(
            id=f"evt_{i+1}",
            type=event_type,
            title=title,
            body=body,
            created_at=datetime.now() - timedelta(hours=i*2),
            read=random.choice([True, False]),
            priority=priority,
            data={}
        ))

    return events

def generate_mock_ticker(ticker: str) -> TickerDetail:
    """Generate mock ticker data"""
    return TickerDetail(
        ticker=ticker,
        company_name=f"{ticker} Inc.",
        sector=random.choice([
            "Technology",
            "Consumer Discretionary",
            "Financials",
            "Healthcare"
        ]),
        market_cap=random.uniform(10e9, 1e12),
        global_score=random.uniform(60, 90),
        in_top_decile=random.choice([True, False]),
        factor_scores=FactorScores(
            leverage=random.uniform(50, 95),
            valuation=random.uniform(50, 95),
            beta=random.uniform(50, 95),
            quality=random.uniform(50, 95),
            growth=random.uniform(50, 95),
            duration=random.uniform(50, 95)
        ),
        theme_scores={
            "high_beta_consumer": random.uniform(60, 90),
            "unprofitable_growth": random.uniform(40, 70)
        },
        primary_theme="high_beta_consumer",
        days_in_top_decile=random.randint(1, 30)
    )

# API Endpoints

@app.get("/")
async def root():
    return {"message": "ShortScreen API", "version": "1.0.0"}

@app.get("/api/v1/status", response_model=StatusResponse)
async def get_status():
    """Get current status and regime"""
    return generate_mock_status()

@app.get("/api/v1/events", response_model=EventsResponse)
async def get_events(
    days: int = Query(7, ge=1, le=30),
    type: Optional[str] = None,
    unread: Optional[bool] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    """Get events/alerts feed"""
    all_events = generate_mock_events()

    # Filter
    if type:
        all_events = [e for e in all_events if e.type == type]
    if unread is not None:
        all_events = [e for e in all_events if e.read != unread]

    # Pagination
    start = (page - 1) * per_page
    end = start + per_page
    events = all_events[start:end]

    return EventsResponse(
        events=events,
        pagination={
            "total": len(all_events),
            "page": page,
            "per_page": per_page
        }
    )

@app.get("/api/v1/events/{event_id}", response_model=Event)
async def get_event(event_id: str):
    """Get single event detail"""
    # Mock implementation
    events = generate_mock_events()
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/api/v1/events/{event_id}/read")
async def mark_event_read(event_id: str):
    """Mark event as read"""
    return {"success": True}

@app.get("/api/v1/tickers/{ticker}", response_model=TickerDetail)
async def get_ticker(ticker: str):
    """Get ticker details"""
    return generate_mock_ticker(ticker.upper())

@app.get("/api/v1/tickers/{ticker}/history")
async def get_ticker_history(ticker: str, days: int = 30):
    """Get ticker score history"""
    history = []
    for i in range(days):
        history.append({
            "date": (datetime.now() - timedelta(days=i)).isoformat(),
            "global_score": random.uniform(60, 90),
            "in_top_decile": random.choice([True, False])
        })
    return {"history": history[::-1]}

# Push Notification Test Endpoint

@app.post("/api/v1/test/push-notification")
async def test_push_notification(
    token: str,
    title: str = "Test Notification",
    body: str = "This is a test push notification"
):
    """
    Test endpoint for push notifications

    In production, this would use FCM/APNs to send actual notifications
    """
    print(f"Would send push notification to {token}:")
    print(f"  Title: {title}")
    print(f"  Body: {body}")

    return {
        "success": True,
        "message": "Push notification sent (mock)",
        "data": {
            "token": token,
            "title": title,
            "body": body,
            "sent_at": datetime.now().isoformat()
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
