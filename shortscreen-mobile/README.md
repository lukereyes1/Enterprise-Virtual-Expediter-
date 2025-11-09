# ShortScreen Command - Mobile App

Mobile-first control panel for real-time short screening signals with deep-dive analytics on demand.

## Overview

"ShortScreen Command" transforms the ShortScreen backend analytics engine into an actionable mobile experience focused on:
- **10-second status check**: Quick regime and theme glance
- **Smart alerts**: Only when signals matter
- **2-minute investigation**: Deep-dive into tickers and themes
- **Zero noise**: Intelligent throttling and aggregation

## Architecture

```
shortscreen-mobile/
├── src/
│   ├── api/
│   │   └── client.ts              # Type-safe API client
│   ├── components/
│   │   ├── EventCard.tsx          # Alert/event card
│   │   ├── FactorBarChart.tsx     # Factor scores visualization
│   │   └── ThemeTile.tsx          # Theme summary tile
│   ├── navigation/
│   ├── screens/
│   │   ├── HomeScreen.tsx         # Dashboard (implemented)
│   │   ├── AlertsScreen.tsx       # Alerts feed (TODO)
│   │   ├── ThemesScreen.tsx       # Theme dashboards (TODO)
│   │   ├── TickerDetailScreen.tsx # Ticker drill-down (TODO)
│   │   ├── WatchlistsScreen.tsx   # Watchlists (TODO)
│   │   └── SettingsScreen.tsx     # Settings (TODO)
│   ├── types/
│   │   └── index.ts               # TypeScript definitions
│   └── utils/
├── backend/
│   ├── main.py                    # FastAPI server (mock data)
│   ├── requirements.txt
│   └── README.md
├── App.tsx                        # Entry point
├── package.json
└── tsconfig.json
```

## Tech Stack

**Mobile:**
- React Native + Expo
- TypeScript
- React Navigation (tabs + stack)
- Axios (HTTP client)
- Victory Native (charts)

**Backend (Stub):**
- FastAPI
- Pydantic
- Mock data generation

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+ (for backend)
- Expo CLI: `npm install -g expo-cli`
- iOS Simulator (Mac) or Android Emulator

### Setup

**1. Install Mobile Dependencies**

```bash
cd shortscreen-mobile
npm install
```

**2. Start Backend Server**

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs at `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`

**3. Start Mobile App**

```bash
cd shortscreen-mobile
npm start
```

Then:
- Press `i` for iOS simulator
- Press `a` for Android emulator
- Scan QR code for physical device

## Screens

### ✅ Implemented

**Home/Dashboard**
- Global regime indicator (Risk-Off/Neutral/Risk-On)
- Theme heatmap with scores and trends
- Top 5 recent signals
- Pull-to-refresh

### 🚧 To Implement

**Alerts Feed**
- Chronological event list
- Filter by type (regime, theme, ticker, system)
- Unread indicator
- Deep-link to detail sheets

**Themes Dashboard**
- Swipeable theme cards
- Per-theme tabs: Overview, Names, History
- Sector distribution charts
- Factor averages vs universe

**Ticker Detail**
- Factor bar chart
- Theme scores and membership
- 30-day score history
- Watchlist actions

**Watchlists**
- Multiple watchlist support
- Aggregated stats (avg score, theme distribution)
- Alert settings per watchlist
- Swipe-to-add functionality

**Settings**
- Notification preferences
- Alert type toggles
- Noise control (max alerts/day, digest mode)
- Account management

## Components

### ✅ Implemented

**FactorBarChart** (`src/components/FactorBarChart.tsx`)
- Horizontal bar chart for 6 factor scores
- Color-coded by factor type
- Responsive layout

**ThemeTile** (`src/components/ThemeTile.tsx`)
- Score display with color gradient
- Trend arrow (up/down/flat)
- Top decile count
- 24h change indicator

**EventCard** (`src/components/EventCard.tsx`)
- Type-specific icons and colors
- Unread indicator
- Time ago formatting
- Priority display

### 🚧 To Implement

- `TickerRow`: Swipeable ticker list item
- `RegimeCard`: Expandable regime detail
- `ScoreHistory`: Line chart component
- `SectorDistribution`: Horizontal bar chart
- `AlertSheet`: Bottom sheet for event details

## API Client

Type-safe client in `src/api/client.ts`:

```typescript
import api from './api/client';

// Get status
const status = await api.getStatus();

// Get events
const events = await api.getEvents({ days: 7, unread: true });

// Get ticker
const ticker = await api.getTicker('TSLA');

// Add to watchlist
await api.addTickerToWatchlist(watchlistId, 'TSLA');
```

All methods return typed responses matching backend schema.

## Type Safety

Complete TypeScript types in `src/types/index.ts`:

```typescript
- StatusResponse
- Event, EventsResponse
- ThemeDetail, ThemeSummary
- TickerDetail, FactorScores
- Watchlist, UserPreferences
- Navigation types
```

## Backend API

Mock FastAPI server serving realistic data:

**Endpoints:**
- `GET /api/v1/status` - Dashboard data
- `GET /api/v1/events` - Alert feed
- `GET /api/v1/tickers/{ticker}` - Ticker details
- `POST /api/v1/test/push-notification` - Test notifications

See `backend/README.md` for full API documentation.

## Navigation

**Tab Bar (Bottom):**
1. Home (Dashboard)
2. Alerts (Activity Feed)
3. Themes (Theme Dashboards)
4. Watchlists
5. Settings

**Modal Screens:**
- Ticker Detail
- Theme Detail
- Watchlist Detail
- Event Detail

## Data Flow

```
Mobile App
    ↓ HTTP Request
API Client (axios)
    ↓ JSON
FastAPI Backend (Mock)
    ↓ (Future: Real data)
ShortScreen Engine
```

## Development

### Running Tests

```bash
npm test
```

### Type Checking

```bash
npm run type-check
```

### Linting

```bash
npm run lint
```

## Next Steps

### Phase 1: Complete Screens (1-2 weeks)
- [ ] Alerts screen with filtering
- [ ] Themes screen with swipeable cards
- [ ] Ticker detail screen
- [ ] Watchlists CRUD
- [ ] Settings screen

### Phase 2: Charts & Visualizations (1 week)
- [ ] Score history line charts
- [ ] Sector distribution bars
- [ ] Theme comparison charts
- [ ] Sparklines for trends

### Phase 3: Push Notifications (1 week)
- [ ] FCM/APNs integration
- [ ] Local notification handling
- [ ] Deep linking from notifications
- [ ] Badge counts

### Phase 4: Polish & Features (1-2 weeks)
- [ ] Offline mode with caching
- [ ] Pull-to-refresh everywhere
- [ ] Swipe gestures (add to watchlist)
- [ ] Haptic feedback
- [ ] Dark mode support
- [ ] Performance optimization

### Phase 5: Real Backend Integration (1 week)
- [ ] Connect to production API
- [ ] Authentication flow
- [ ] Error handling
- [ ] Rate limiting
- [ ] Caching strategy

### Phase 6: Launch (1 week)
- [ ] Beta testing
- [ ] App store assets
- [ ] Privacy policy
- [ ] Terms of service
- [ ] App store submission

## Design Principles

**Mobile-First:**
- Touch-optimized interfaces
- Fast load times (<2s)
- Offline-capable
- Native gestures

**Information Density:**
- Most important data above the fold
- Progressive disclosure
- Smart defaults
- Contextual actions

**Zero Noise:**
- Intelligent alert throttling (max 20/day)
- Aggregation windows (5 min)
- Digest mode option
- Market hours filtering

**Visual Hierarchy:**
- Color for status (red=risk-off, green=risk-on)
- Size for importance
- Position for priority
- Animation for attention

## Screenshots

(Screenshots will be added as screens are completed)

## License

MIT

## Contributing

1. Follow existing code patterns
2. Use TypeScript types everywhere
3. Test on both iOS and Android
4. Update this README for new features
