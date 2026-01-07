# OYL Status Page

A full-stack status page application to monitor the uptime and health status of OYL endpoints.

## Features

- **Real-time Health Monitoring**: Monitors multiple API endpoints every 5 minutes
- **Status Banner**: Displays overall system status (All Systems Operational, Partial Outage, Major Outage)
- **90-Day Uptime History**: Visual representation of uptime for each endpoint over the last 90 days
- **Response Time Tracking**: Shows the latest response time for each endpoint
- **Manual Refresh**: Ability to trigger health checks on demand

## Monitored Endpoints

1. **Sandshrew Mainnet API** - `https://mainnet.sandshrew.io/v2`
2. **Metashrew API** - `https://metashrew.s.oyl.gg`
3. **Alkanes API** - `https://alkanes.oyl.gg`
4. **OYL App** - `https://app.oyl.io`

## Tech Stack

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS
- **Backend**: FastAPI with Python
- **Database**: SQLite

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | API health check |
| `/api/status` | GET | Get overall status and all endpoint statuses |
| `/api/endpoints` | GET | List all monitored endpoints |
| `/api/endpoints/{id}/history` | GET | Get 90-day uptime history for an endpoint |
| `/api/endpoints/{id}/checks` | GET | Get recent health checks for an endpoint |
| `/api/check-now` | POST | Trigger immediate health check for all endpoints |

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI application
│   │   ├── database.py       # Database configuration
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── health_checker.py # Health check logic
│   │   └── seed_endpoints.py # Endpoint configuration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── EndpointCard.tsx
│   │   │   ├── StatusBanner.tsx
│   │   │   ├── StatusPage.tsx
│   │   │   └── UptimeBar.tsx
│   │   ├── lib/
│   │   │   └── api.ts
│   │   └── types/
│   │       └── index.ts
│   ├── package.json
│   ├── tailwind.config.js
│   └── next.config.js
└── README.md
```

## Configuration

### Adding New Endpoints

Edit `backend/app/seed_endpoints.py` to add or modify monitored endpoints:

```python
ENDPOINTS_CONFIG = [
    {
        "name": "My API",
        "url": "https://api.example.com/health",
        "method": "GET",
        "headers": None,
        "body": None,
        "expected_status": 200,
    },
]
```

### Adjusting Check Interval

In `backend/app/main.py`, modify the scheduler interval:

```python
scheduler.add_job(sync_run_health_checks, 'interval', minutes=5)  # Change to desired interval
```

## License

MIT
