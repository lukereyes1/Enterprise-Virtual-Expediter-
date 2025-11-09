# ShortScreen Command - Mobile App Architecture

## Vision

"ShortScreen Command" - A mobile-first control panel for real-time short screening signals with deep-dive analytics on demand.

**Design Principle:** 10-second status check, 2-minute investigation, zero noise alerts.

---

## Core Use Cases

### 1. Quick Status (< 10 seconds)
**User Story:** "Is the model flashing risk-on or risk-off right now? Which themes are lighting up?"

**Flow:**
1. Open app → Dashboard loads
2. See regime indicator (Risk-Off / Neutral / Risk-On)
3. Glance at 4 theme tiles with scores + trend arrows
4. Check top 3-5 recent events
5. Done

**API Calls:** 1 (GET /api/v1/status)

### 2. Alerts That Matter
**User Story:** "Notify me when regime flips or theme goes critical, only when it matters."

**Flow:**
1. Push notification arrives: "Risk regime changed: Neutral → Risk-Off"
2. Tap notification → Deep link to dashboard with highlight
3. See before/after metrics + sparkline
4. Optionally drill into affected themes/tickers
5. Done

**Smart Throttling:**
- Max 20 push notifications/day
- Aggregate similar events (5 min window)
- Regime changes: Only on band transitions
- Theme spikes: Only on significant deltas (>10 points)
- Ticker alerts: Max 1/ticker/day unless regime change

### 3. Lightweight Investigation
**User Story:** "Tap an alert, see why the model is saying this. Check factor breakdown for a ticker."

**Flow:**
1. From alert feed → Tap ticker alert
2. Ticker detail screen loads
3. See factor breakdown (bars), theme scores, history chart
4. Understand reasoning in 30 seconds
5. Add to watchlist or dismiss
6. Done

**API Calls:** 2 (GET /api/v1/tickers/{ticker}, GET /api/v1/tickers/{ticker}/history)

### 4. Asynchronous Reporting
**User Story:** "Daily wrap-up digest. On-demand scan with macro sliders."

**Flow (Daily):**
1. 5:30 PM ET: Push notification "Daily report ready"
2. Tap → Opens report view
3. See charts, metrics, top movers
4. Export to CSV if needed
5. Done

**Flow (On-Demand):**
1. Open "Run Scan" screen
2. Adjust macro sliders (downturn, inflation, liquidity)
3. Tap "Run" → Job queued
4. Get push when complete
5. Tap → View results
6. Done

---

## Screen Architecture

### Navigation Structure

```
TabBar (Bottom)
├── 🏠 Home (Dashboard)
├── 🔔 Alerts (Activity Feed)
├── 📊 Themes (Theme Dashboards)
├── ⭐ Watchlists
└── ⚙️ Settings

Modal Screens
├── Ticker Detail (from anywhere)
├── Report Viewer (from notifications)
└── Scan Runner (from + button)
```

---

## Screen Specifications

### A. Home / Dashboard

**Purpose:** One-glance model state

**Layout:**
```
┌─────────────────────────────────────┐
│ ShortScreen Command        [⚙️] [+] │
├─────────────────────────────────────┤
│ GLOBAL REGIME                       │
│ ┌─────────────────────────────────┐ │
│ │ 🔴 Risk-Off                     │ │
│ │ Based on beta, leverage, stress │ │
│ │ [████████████░░░░░░░] 0.78     │ │
│ └─────────────────────────────────┘ │
│                                     │
│ THEME HEATMAP                       │
│ ┌──────────┬──────────┬──────────┐ │
│ │Unprofitbl│OverLev  │HighBeta │ │
│ │ Growth   │SmallCaps│ Consumer│ │
│ │   72 ↗️   │   68 ↗️  │   81 ↗️  │ │
│ │  23 names│ 18 names│ 31 names│ │
│ └──────────┴──────────┴──────────┘ │
│ ┌──────────┐                       │
│ │  Weak    │                       │
│ │Financials│                       │
│ │   65 ↘️   │                       │
│ │ 15 names │                       │
│ └──────────┘                       │
│                                     │
│ TOP SIGNALS                         │
│ ┌─────────────────────────────────┐ │
│ │ 🔵 5 new names joined Unprofitbl│ │
│ │    Growth top decile      2h ago│ │
│ │ 🟡 Small Cap Stress 0.62 → 0.75 │ │
│ │                           4h ago│ │
│ │ 🔴 AAPL entered top decile      │ │
│ │                           6h ago│ │
│ └─────────────────────────────────┘ │
│                                     │
│ [View Full Report]                  │
└─────────────────────────────────────┘
```

**API Endpoints:**
- `GET /api/v1/status` → Regime, themes, recent events
- `GET /api/v1/events?limit=5&type=recent` → Top signals

**Components:**
- `RegimeCard`: Traffic light + meter + subtext
- `ThemeHeatmap`: Grid of theme tiles
- `ThemeTile`: Score, trend arrow, count
- `EventsList`: Chronological feed preview

**Refresh:**
- Pull-to-refresh
- Auto-refresh every 5 minutes when app is active
- Background fetch when inactive (iOS/Android)

### B. Alerts & Activity Feed

**Purpose:** Notification log with drill-down

**Layout:**
```
┌─────────────────────────────────────┐
│ Alerts              [Filter] [Mark] │
├─────────────────────────────────────┤
│ TODAY                               │
│ ┌─────────────────────────────────┐ │
│ │ 🔴 REGIME  Risk regime changed  │ │
│ │    Neutral → Risk-Off     2h ago│ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 🔵 THEME   Unprofitable Growth  │ │
│ │    +5 top decile names    4h ago│ │
│ └─────────────────────────────────┘ │
│                                     │
│ YESTERDAY                           │
│ ┌─────────────────────────────────┐ │
│ │ ⭐ TICKER  TSLA entered top     │ │
│ │    decile (watchlist)    20h ago│ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 🟡 THEME   High Beta Consumer   │ │
│ │    Score spike 65 → 78   22h ago│ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Alert Types & Icons:**
- 🔴 Regime changes
- 🔵 Theme spikes
- ⭐ Ticker events (watchlist)
- 🟡 Theme membership changes
- ⚠️ System events (degraded mode)

**Detail Overlays (Bottom Sheet):**

**Regime Change:**
```
┌─────────────────────────────────────┐
│ Risk Regime Changed                 │
├─────────────────────────────────────┤
│ Neutral → Risk-Off                  │
│                                     │
│ BEFORE          NOW                 │
│ Risk-Off: 0.52  Risk-Off: 0.78 ↗️   │
│ SmallCap: 0.48  SmallCap: 0.63 ↗️   │
│ Avg Beta: 1.32  Avg Beta: 1.51 ↗️   │
│                                     │
│ [──────────────────────────]        │
│ Last 7 days regime trend            │
│                                     │
│ [View Dashboard]        [Dismiss]   │
└─────────────────────────────────────┘
```

**Theme Spike:**
```
┌─────────────────────────────────────┐
│ Unprofitable Growth                 │
├─────────────────────────────────────┤
│ Score: 65 → 72 (+7)                 │
│                                     │
│ NEW TOP DECILE ENTRANTS             │
│ SNOW  Software      $15.2B          │
│ DDOG  Software      $12.8B          │
│ NET   Software      $10.4B          │
│ MDB   Software       $8.9B          │
│ CRWD  Software       $8.1B          │
│                                     │
│ [View Theme Dashboard]  [Dismiss]   │
└─────────────────────────────────────┘
```

**Ticker Alert:**
```
┌─────────────────────────────────────┐
│ TSLA - Tesla, Inc.                  │
├─────────────────────────────────────┤
│ Consumer Discretionary  |  $850.2B  │
│                                     │
│ ENTERED TOP DECILE                  │
│ Global Vulnerability: 78.4          │
│                                     │
│ FACTOR SCORES                       │
│ Leverage    [█████████░] 87         │
│ Valuation   [████████░░] 76         │
│ Beta        [████████░░] 82         │
│ Duration    [██████░░░░] 65         │
│                                     │
│ PRIMARY THEME                       │
│ High Beta Consumer (Score: 81.2)    │
│                                     │
│ [View Full Detail]      [Dismiss]   │
└─────────────────────────────────────┘
```

**API Endpoints:**
- `GET /api/v1/events?days=7` → Alert feed
- `GET /api/v1/events/{eventId}` → Event detail
- `POST /api/v1/events/{eventId}/read` → Mark as read

### C. Themes Dashboard

**Purpose:** Portfolio-level view by theme

**Layout (List View):**
```
┌─────────────────────────────────────┐
│ Themes              [Grid] [List]   │
├─────────────────────────────────────┤
│ Swipe cards horizontally →          │
│ ┌─────────────────────────────────┐ │
│ │ UNPROFITABLE GROWTH             │ │
│ │ ───────────────────────────────  │ │
│ │ Score: 72 ↗️    23 names         │ │
│ │                                  │ │
│ │ SECTOR DISTRIBUTION              │ │
│ │ Tech    [████████░░] 18          │ │
│ │ Health  [████░░░░░░]  5          │ │
│ │                                  │ │
│ │ [Overview] [Names] [History]     │ │
│ └─────────────────────────────────┘ │
│    ●○○○ (swipe indicators)          │
└─────────────────────────────────────┘
```

**Per-Theme Tabs:**

**Tab 1: Overview**
```
What this theme captures:
High-growth, unprofitable companies
vulnerable to valuation compression.

KEY FACTORS VS UNIVERSE
Valuation    [████████░░] +25% higher
Profitability[██████████] -80% lower
Growth       [███████░░░] +45% higher
```

**Tab 2: Names**
```
┌─────────────────────────────────────┐
│ Sort: [Global Score ▼]              │
├─────────────────────────────────────┤
│ SNOW  Software         $15.2B       │
│ ├─ Global: 84.2  Theme: 89.5        │
│ └─ [→ Watchlist]                    │
│                                     │
│ DDOG  Software         $12.8B       │
│ ├─ Global: 81.7  Theme: 87.3        │
│ └─ [→ Watchlist]                    │
│                                     │
│ (Swipe right to add to watchlist)   │
└─────────────────────────────────────┘
```

**Tab 3: History**
```
Theme Score (Last 30 Days)
[Line chart: 62 → 68 → 65 → 72]

Top Decile Count (Last 30 Days)
[Area chart: 18 → 21 → 20 → 23]
```

**API Endpoints:**
- `GET /api/v1/themes` → List all themes
- `GET /api/v1/themes/{themeName}` → Theme details
- `GET /api/v1/themes/{themeName}/names` → Names in theme
- `GET /api/v1/themes/{themeName}/history?days=30` → Historical data

### D. Ticker Detail Screen

**Purpose:** One-glance explanation of ticker ranking

**Layout:**
```
┌─────────────────────────────────────┐
│ ← TSLA                     ⭐ ⚙️    │
├─────────────────────────────────────┤
│ Tesla, Inc.                         │
│ Consumer Discretionary  |  $850.2B  │
│ [TOP DECILE] [WATCHLIST]            │
│                                     │
│ GLOBAL VULNERABILITY                │
│ ┌─────────────────────────────────┐ │
│ │        78.4                     │ │
│ │    [████████████████░░░░]       │ │
│ └─────────────────────────────────┘ │
│                                     │
│ FACTOR SCORES                       │
│ Leverage    [█████████░] 87         │
│ Valuation   [████████░░] 76         │
│ Beta        [████████░░] 82         │
│ Quality     [███████░░░] 71         │
│ Growth      [██████░░░░] 65         │
│ Duration    [██████░░░░] 63         │
│                                     │
│ THEME MEMBERSHIP                    │
│ ● High Beta Consumer      81.2      │
│ ○ Unprofitable Growth     45.3      │
│                                     │
│ HISTORY (30 Days)                   │
│ [Line chart showing score over time]│
│                                     │
│ Days in Top Decile: 12 days         │
│                                     │
│ ACTIONS                             │
│ [Add to Watchlist]                  │
│ [Subscribe to Alerts]               │
└─────────────────────────────────────┘
```

**API Endpoints:**
- `GET /api/v1/tickers/{ticker}` → Ticker details
- `GET /api/v1/tickers/{ticker}/history?days=30` → Score history
- `POST /api/v1/watchlists/{listId}/tickers` → Add to watchlist
- `POST /api/v1/subscriptions/ticker/{ticker}` → Subscribe to alerts

### E. Watchlists

**Purpose:** Focus signals on relevant subset

**Layout:**
```
┌─────────────────────────────────────┐
│ Watchlists                    [+]   │
├─────────────────────────────────────┤
│ MY WATCHLISTS                       │
│ ┌─────────────────────────────────┐ │
│ │ 📌 Priority Shorts              │ │
│ │    12 names  |  Avg Score: 76.3 │ │
│ │    [Alerts: ON] [View →]        │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ 👀 Monitoring                   │ │
│ │    8 names   |  Avg Score: 68.5 │ │
│ │    [Alerts: OFF] [View →]       │ │
│ └─────────────────────────────────┘ │
│                                     │
│ [+ Create New Watchlist]            │
└─────────────────────────────────────┘
```

**Watchlist Detail:**
```
┌─────────────────────────────────────┐
│ ← Priority Shorts        [⚙️] [···] │
├─────────────────────────────────────┤
│ OVERVIEW                            │
│ 12 names  |  Avg Vulnerability: 76.3│
│                                     │
│ THEME DISTRIBUTION                  │
│ High Beta      [██████░░░░]  6      │
│ Unprofitable   [████░░░░░░]  4      │
│ SmallCap Lever [██░░░░░░░░]  2      │
│                                     │
│ ALERT SETTINGS                      │
│ ☑️ Score crosses 80                 │
│ ☑️ Enters/exits top decile          │
│ ☑️ Factor spike (>10 points)        │
│                                     │
│ NAMES                               │
│ ┌─────────────────────────────────┐ │
│ │ TSLA  Consumer Disc.   $850.2B  │ │
│ │ Score: 78.4 ↗️  (Top Decile)     │ │
│ └─────────────────────────────────┘ │
│ ┌─────────────────────────────────┐ │
│ │ SNOW  Software         $15.2B   │ │
│ │ Score: 84.2 ↗️  (Top Decile)     │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

**API Endpoints:**
- `GET /api/v1/watchlists` → User's watchlists
- `POST /api/v1/watchlists` → Create watchlist
- `GET /api/v1/watchlists/{listId}` → Watchlist details
- `PUT /api/v1/watchlists/{listId}/settings` → Update alert settings
- `DELETE /api/v1/watchlists/{listId}/tickers/{ticker}` → Remove ticker

### F. Settings & Notification Rules

**Layout:**
```
┌─────────────────────────────────────┐
│ ← Settings                          │
├─────────────────────────────────────┤
│ ACCOUNT                             │
│ user@example.com                    │
│ [Logout]                            │
│                                     │
│ ALERT PREFERENCES                   │
│ ┌─────────────────────────────────┐ │
│ │ Regime Changes         [ON]     │ │
│ │ Theme Spikes           [ON]     │ │
│ │ New Top Decile Names   [ON]     │ │
│ │ Watchlist Alerts       [ON]     │ │
│ │ System Issues          [ON]     │ │
│ └─────────────────────────────────┘ │
│                                     │
│ NOISE CONTROL                       │
│ Max alerts per day:     [20     ]   │
│ Digest mode:            [OFF]       │
│ Market hours only:      [ON]        │
│                                     │
│ DATA & ENVIRONMENT                  │
│ Provider: Yahoo Finance (Live)      │
│ Last update: 2 minutes ago          │
│ Cache status: [View]                │
│                                     │
│ APP                                 │
│ Version: 1.0.0                      │
│ [Privacy Policy]  [Terms]           │
└─────────────────────────────────────┘
```

**API Endpoints:**
- `GET /api/v1/users/me` → User profile
- `GET /api/v1/users/me/preferences` → Notification preferences
- `PUT /api/v1/users/me/preferences` → Update preferences
- `GET /api/v1/system/status` → System health

---

## Notification Model

### Event Categories & Rules

#### 1. Regime Events
**Trigger:** risk_off_score or small_cap_stress_score crosses band thresholds

**Bands:**
- Low: 0.0 - 0.33
- Medium: 0.34 - 0.66
- High: 0.67 - 1.0

**Rule:** Notify only on band transitions, not minor ticks

**Example:**
```json
{
  "type": "regime_change",
  "title": "Risk regime changed",
  "body": "Neutral → Risk-Off",
  "priority": "high",
  "data": {
    "previous_band": "medium",
    "current_band": "high",
    "risk_off_score": 0.78,
    "small_cap_stress": 0.63,
    "avg_beta": 1.51
  }
}
```

#### 2. Theme Events
**Trigger:**
- Theme score change > 10 points
- Top decile membership change > 5 names

**Aggregation:** Group changes within 5-minute window

**Example:**
```json
{
  "type": "theme_spike",
  "title": "Unprofitable Growth",
  "body": "+5 new top decile names",
  "priority": "medium",
  "data": {
    "theme": "unprofitable_growth",
    "score_change": 7,
    "previous_score": 65,
    "current_score": 72,
    "new_entrants": ["SNOW", "DDOG", "NET", "MDB", "CRWD"],
    "new_entrants_count": 5
  }
}
```

#### 3. Ticker Events
**Trigger:**
- Watchlisted ticker crosses threshold (default: 80)
- Watchlisted ticker enters/exits top decile
- Factor spike > 15 points

**Throttle:** Max 1 alert per ticker per day (unless regime change)

**Example:**
```json
{
  "type": "ticker_alert",
  "title": "TSLA entered top decile",
  "body": "Global score: 78.4 (watchlist: Priority Shorts)",
  "priority": "medium",
  "data": {
    "ticker": "TSLA",
    "watchlist": "priority_shorts",
    "global_score": 78.4,
    "primary_theme": "high_beta_consumer",
    "reason": "entered_top_decile"
  }
}
```

#### 4. System Events
**Trigger:**
- Data provider failure
- Cache-only mode activated
- Job failure

**Priority:** High

**Example:**
```json
{
  "type": "system_alert",
  "title": "Data provider unavailable",
  "body": "Running in cache-only mode",
  "priority": "high",
  "data": {
    "degraded_mode": true,
    "reason": "api_timeout",
    "last_fresh_data": "2024-01-15T16:30:00Z"
  }
}
```

### Frequency Management

**Server-Side Throttling:**

1. **Per-User Hard Cap:** 20 push notifications/day
2. **Aggregation Windows:** 5 minutes for similar events
3. **Digest Mode:** If cap exceeded, switch to digest automatically
4. **Quiet Hours:** Respect user timezone, market hours setting

**Throttling Logic:**
```python
class NotificationThrottle:
    def should_send(user_id, event_type, ticker=None):
        # Check daily cap
        if get_daily_count(user_id) >= user.max_alerts_per_day:
            queue_for_digest(user_id, event)
            return False

        # Check per-ticker throttle
        if ticker and last_alert_for_ticker(user_id, ticker) < 24h:
            return False  # Skip unless regime change

        # Check aggregation window
        if similar_event_in_window(user_id, event_type, window=5min):
            aggregate_events(user_id, event)
            return False

        return True
```

---

## API Specification

### Base URL
```
Production: https://api.shortscreen.com/v1
Staging:    https://api-staging.shortscreen.com/v1
```

### Authentication
All endpoints require JWT token in Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Endpoints

#### Status & Dashboard

**GET /api/v1/status**
Returns current regime and top-level metrics.

Response:
```json
{
  "timestamp": "2024-01-15T16:30:00Z",
  "regime": {
    "status": "risk_off",
    "risk_off_score": 0.78,
    "small_cap_stress_score": 0.63,
    "avg_beta": 1.51
  },
  "themes": [
    {
      "name": "unprofitable_growth",
      "display_name": "Unprofitable Growth",
      "score": 72,
      "trend": "up",
      "top_decile_count": 23,
      "score_change_24h": 7
    },
    // ... other themes
  ],
  "data_freshness": {
    "fundamentals_updated_at": "2024-01-15T09:00:00Z",
    "market_data_updated_at": "2024-01-15T16:28:00Z"
  }
}
```

**GET /api/v1/events**
Returns alert feed.

Query params:
- `days`: Number of days to retrieve (default: 7)
- `type`: Filter by event type
- `unread`: Boolean, unread only

Response:
```json
{
  "events": [
    {
      "id": "evt_123",
      "type": "regime_change",
      "title": "Risk regime changed",
      "body": "Neutral → Risk-Off",
      "created_at": "2024-01-15T14:30:00Z",
      "read": false,
      "priority": "high",
      "data": { /* event-specific data */ }
    },
    // ... more events
  ],
  "pagination": {
    "total": 45,
    "page": 1,
    "per_page": 20
  }
}
```

#### Themes

**GET /api/v1/themes**
List all themes with current scores.

**GET /api/v1/themes/{themeName}**
Get theme details.

Response:
```json
{
  "name": "unprofitable_growth",
  "display_name": "Unprofitable Growth",
  "description": "High-growth, unprofitable companies vulnerable to valuation compression",
  "score": 72,
  "top_decile_count": 23,
  "sector_distribution": {
    "Technology": 18,
    "Healthcare": 5
  },
  "factor_vs_universe": {
    "valuation": 1.25,  // 25% higher
    "profitability": -0.80,  // 80% lower
    "growth": 1.45
  }
}
```

**GET /api/v1/themes/{themeName}/names**
Get names in theme.

Query params:
- `sort`: Sort field (global_score, theme_score)
- `limit`: Number of results

Response:
```json
{
  "names": [
    {
      "ticker": "SNOW",
      "company_name": "Snowflake Inc.",
      "sector": "Software",
      "market_cap": 15200000000,
      "global_score": 84.2,
      "theme_score": 89.5,
      "in_top_decile": true
    },
    // ... more names
  ]
}
```

**GET /api/v1/themes/{themeName}/history**
Historical theme data.

Query params:
- `days`: Lookback period (default: 30)

Response:
```json
{
  "history": [
    {
      "date": "2024-01-15",
      "score": 72,
      "top_decile_count": 23
    },
    // ... more days
  ]
}
```

#### Tickers

**GET /api/v1/tickers/{ticker}**
Get ticker details.

Response:
```json
{
  "ticker": "TSLA",
  "company_name": "Tesla, Inc.",
  "sector": "Consumer Discretionary",
  "market_cap": 850200000000,
  "global_score": 78.4,
  "in_top_decile": true,
  "factor_scores": {
    "leverage": 87,
    "valuation": 76,
    "beta": 82,
    "quality": 71,
    "growth": 65,
    "duration": 63
  },
  "theme_scores": {
    "high_beta_consumer": 81.2,
    "unprofitable_growth": 45.3
  },
  "primary_theme": "high_beta_consumer",
  "days_in_top_decile": 12
}
```

**GET /api/v1/tickers/{ticker}/history**
Score history for ticker.

Response:
```json
{
  "history": [
    {
      "date": "2024-01-15",
      "global_score": 78.4,
      "in_top_decile": true
    },
    // ... more days
  ]
}
```

#### Watchlists

**GET /api/v1/watchlists**
Get user's watchlists.

**POST /api/v1/watchlists**
Create new watchlist.

Request:
```json
{
  "name": "Priority Shorts",
  "description": "High conviction shorts",
  "alert_settings": {
    "score_threshold": 80,
    "notify_on_entry": true,
    "notify_on_exit": true,
    "notify_on_factor_spike": true
  }
}
```

**GET /api/v1/watchlists/{listId}**
Get watchlist details.

**POST /api/v1/watchlists/{listId}/tickers**
Add ticker to watchlist.

Request:
```json
{
  "ticker": "TSLA"
}
```

**DELETE /api/v1/watchlists/{listId}/tickers/{ticker}**
Remove ticker from watchlist.

#### User Preferences

**GET /api/v1/users/me/preferences**
Get notification preferences.

Response:
```json
{
  "alert_types": {
    "regime_changes": true,
    "theme_spikes": true,
    "new_top_decile": true,
    "watchlist_alerts": true,
    "system_issues": true
  },
  "max_alerts_per_day": 20,
  "digest_mode": false,
  "market_hours_only": true,
  "timezone": "America/New_York"
}
```

**PUT /api/v1/users/me/preferences**
Update preferences.

---

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                     Mobile Apps                          │
│         iOS (Swift/SwiftUI) + Android (Kotlin)          │
│              or React Native / Flutter                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTPS / REST API
                     │
┌────────────────────▼────────────────────────────────────┐
│                  API Gateway                             │
│  - Authentication (JWT)                                  │
│  - Rate limiting                                         │
│  - Request routing                                       │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼────────┐ ┌─▼──────────┐
│ API Server   │ │ Notif     │ │ ShortScreen│
│              │ │ Service   │ │   Engine   │
│ - Endpoints  │ │           │ │            │
│ - Business   │ │ - Event   │ │ - Jobs     │
│   logic      │ │   detection│ │ - Scoring  │
│ - Data layer │ │ - Throttle │ │ - Cache    │
└──────┬───────┘ └─────┬─────┘ └─────┬──────┘
       │               │             │
       │               │             │
┌──────▼───────────────▼─────────────▼──────┐
│          PostgreSQL Database               │
│  - Users, watchlists, preferences          │
│  - Events, alerts                          │
│  - Scores, themes (denormalized)           │
│  - Historical data                         │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│         Push Notification Services         │
│  - APNs (Apple Push Notification service)  │
│  - FCM (Firebase Cloud Messaging)          │
└────────────────────────────────────────────┘
```

### Database Schema

**Users Table:**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  timezone VARCHAR(50) DEFAULT 'America/New_York',
  push_token VARCHAR(255),  -- FCM/APNs token
  platform VARCHAR(10)       -- 'ios' or 'android'
);
```

**Preferences Table:**
```sql
CREATE TABLE user_preferences (
  user_id UUID REFERENCES users(id),
  alert_regime_changes BOOLEAN DEFAULT true,
  alert_theme_spikes BOOLEAN DEFAULT true,
  alert_new_top_decile BOOLEAN DEFAULT true,
  alert_watchlist BOOLEAN DEFAULT true,
  alert_system_issues BOOLEAN DEFAULT true,
  max_alerts_per_day INT DEFAULT 20,
  digest_mode BOOLEAN DEFAULT false,
  market_hours_only BOOLEAN DEFAULT true,
  PRIMARY KEY (user_id)
);
```

**Watchlists Table:**
```sql
CREATE TABLE watchlists (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name VARCHAR(100) NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  alert_score_threshold INT DEFAULT 80,
  alert_on_entry BOOLEAN DEFAULT true,
  alert_on_exit BOOLEAN DEFAULT true,
  alert_on_factor_spike BOOLEAN DEFAULT true
);

CREATE TABLE watchlist_tickers (
  watchlist_id UUID REFERENCES watchlists(id),
  ticker VARCHAR(10) NOT NULL,
  added_at TIMESTAMP DEFAULT NOW(),
  PRIMARY KEY (watchlist_id, ticker)
);
```

**Events Table:**
```sql
CREATE TABLE events (
  id UUID PRIMARY KEY,
  type VARCHAR(50) NOT NULL,  -- regime_change, theme_spike, etc.
  title VARCHAR(255) NOT NULL,
  body TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  priority VARCHAR(10) DEFAULT 'medium',
  data JSONB,  -- Event-specific data
  INDEX idx_created_at (created_at DESC),
  INDEX idx_type (type)
);

CREATE TABLE user_events (
  user_id UUID REFERENCES users(id),
  event_id UUID REFERENCES events(id),
  read BOOLEAN DEFAULT false,
  notified BOOLEAN DEFAULT false,
  notified_at TIMESTAMP,
  PRIMARY KEY (user_id, event_id)
);
```

**Scores Cache (Denormalized):**
```sql
CREATE TABLE ticker_scores (
  ticker VARCHAR(10) NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  global_score FLOAT NOT NULL,
  in_top_decile BOOLEAN,
  factor_scores JSONB,
  theme_scores JSONB,
  primary_theme VARCHAR(50),
  PRIMARY KEY (ticker, timestamp),
  INDEX idx_timestamp (timestamp DESC),
  INDEX idx_global_score (global_score DESC)
);

CREATE TABLE theme_scores (
  theme_name VARCHAR(50) NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  score FLOAT NOT NULL,
  top_decile_count INT,
  sector_distribution JSONB,
  PRIMARY KEY (theme_name, timestamp),
  INDEX idx_timestamp (timestamp DESC)
);

CREATE TABLE regime_history (
  timestamp TIMESTAMP PRIMARY KEY,
  status VARCHAR(20),  -- risk_off, neutral, risk_on
  risk_off_score FLOAT,
  small_cap_stress_score FLOAT,
  avg_beta FLOAT
);
```

### Technology Stack

**Backend:**
- **Language:** Python 3.11+
- **API Framework:** FastAPI (async, OpenAPI docs)
- **Database:** PostgreSQL 14+
- **ORM:** SQLAlchemy 2.0 (async)
- **Job Queue:** Celery + Redis
- **Caching:** Redis
- **Push Notifications:**
  - APNs via `aioapns`
  - FCM via `firebase-admin`

**Mobile:**
- **Framework:** React Native (TypeScript)
  - Single codebase for iOS + Android
  - Native performance
  - Large ecosystem
- **State Management:** Redux Toolkit
- **Navigation:** React Navigation
- **Charts:** Victory Native (or recharts-native)
- **Push:** react-native-push-notification

**Infrastructure:**
- **Hosting:** AWS / GCP
- **Container:** Docker
- **Orchestration:** Kubernetes (optional) or ECS
- **CI/CD:** GitHub Actions
- **Monitoring:** Datadog / Sentry

---

## Implementation Roadmap

### Phase 1: API Foundation (Week 1-2)
- [ ] FastAPI server setup
- [ ] Database schema implementation
- [ ] Authentication (JWT)
- [ ] Core endpoints:
  - Status/dashboard
  - Events feed
  - Themes list/detail
  - Ticker detail
- [ ] Integration with existing ShortScreen engine
- [ ] API documentation (OpenAPI/Swagger)

### Phase 2: Event System (Week 2-3)
- [ ] Event detection logic
- [ ] Event queue implementation
- [ ] Notification service
- [ ] Throttling/aggregation logic
- [ ] Push notification integration (APNs/FCM)
- [ ] Testing with mock events

### Phase 3: Mobile App Core (Week 3-5)
- [ ] React Native project setup
- [ ] Navigation structure
- [ ] API client layer
- [ ] Authentication flow
- [ ] Dashboard screen
- [ ] Alerts feed screen
- [ ] Push notification handling
- [ ] Deep linking

### Phase 4: Advanced Screens (Week 5-7)
- [ ] Themes dashboard
- [ ] Ticker detail screen
- [ ] Watchlists CRUD
- [ ] Settings screen
- [ ] Chart implementations
- [ ] Swipe gestures
- [ ] Pull-to-refresh

### Phase 5: Polish & Launch (Week 7-8)
- [ ] UI/UX refinement
- [ ] Error handling
- [ ] Offline mode
- [ ] Performance optimization
- [ ] Testing (unit, integration, E2E)
- [ ] App store preparation
- [ ] Beta testing
- [ ] Launch!

---

## Success Metrics

**Engagement:**
- Daily active users
- Average session duration
- Screens per session
- Alert open rate

**Performance:**
- API response time (p95 < 200ms)
- App launch time (< 2s)
- Dashboard load time (< 1s)

**Reliability:**
- API uptime (99.9%+)
- Push delivery rate (> 95%)
- Error rate (< 0.1%)

**User Satisfaction:**
- App store rating (> 4.5)
- Alert usefulness rating
- Feature usage distribution

---

This architecture provides a complete blueprint for "ShortScreen Command" - a mobile-first platform that delivers actionable signals with minimal noise and maximum clarity.
