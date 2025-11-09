# ShortScreen API Backend Stub

Mock FastAPI backend for ShortScreen Command mobile app development and testing.

## Features

- ✅ RESTful API matching production schema
- ✅ Mock data generation for all endpoints
- ✅ CORS enabled for mobile app
- ✅ OpenAPI/Swagger documentation
- ✅ Push notification test endpoint

## Setup

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Run Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Available Endpoints

### Status & Dashboard
- `GET /api/v1/status` - Current regime and theme scores

### Events
- `GET /api/v1/events` - Alert feed with filtering
- `GET /api/v1/events/{event_id}` - Event detail
- `POST /api/v1/events/{event_id}/read` - Mark as read

### Tickers
- `GET /api/v1/tickers/{ticker}` - Ticker details
- `GET /api/v1/tickers/{ticker}/history` - Score history

### Testing
- `POST /api/v1/test/push-notification` - Test push notifications

## Mock Data

All endpoints return realistic mock data that matches the production API schema:

- Random but consistent data generation
- Proper timestamps and relationships
- Realistic score ranges (0-100)
- Multiple themes, tickers, events

## Next Steps

To integrate with real ShortScreen engine:

1. Replace mock data generators with actual database queries
2. Add authentication/authorization
3. Implement real push notification service (FCM/APNs)
4. Add rate limiting
5. Connect to ShortScreen job system

## Mobile App Configuration

Point the mobile app to this backend:

```typescript
// src/api/client.ts
const API_BASE_URL = 'http://localhost:8000/api/v1';  // Development
// const API_BASE_URL = 'https://api.shortscreen.com/v1';  // Production
```

For iOS Simulator, use `http://localhost:8000`
For Android Emulator, use `http://10.0.2.2:8000`
For physical devices, use your machine's IP: `http://192.168.x.x:8000`
