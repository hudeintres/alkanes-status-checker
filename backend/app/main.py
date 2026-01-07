from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from .database import engine, get_db, Base
from .models import Endpoint, HealthCheck
from .schemas import (
    EndpointResponse,
    HealthCheckResponse,
    EndpointStatus,
    DailyUptime,
    EndpointHistory,
    OverallStatus,
)
from .health_checker import sync_run_health_checks, run_health_checks
from .seed_endpoints import seed_endpoints
import asyncio

# Create tables
Base.metadata.create_all(bind=engine)

# Scheduler for periodic health checks
scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    seed_endpoints()
    
    # Run initial health check
    await run_health_checks()
    
    # Schedule health checks every 5 minutes
    scheduler.add_job(sync_run_health_checks, 'interval', minutes=5)
    scheduler.start()
    
    yield
    
    # Shutdown
    scheduler.shutdown()


app = FastAPI(
    title="Status Page API",
    description="API for monitoring endpoint health and uptime",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """API health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/endpoints", response_model=List[EndpointResponse])
async def get_endpoints(db: Session = Depends(get_db)):
    """Get all monitored endpoints."""
    endpoints = db.query(Endpoint).all()
    return endpoints


@app.get("/api/status", response_model=OverallStatus)
async def get_overall_status(db: Session = Depends(get_db)):
    """Get overall status and current status of all endpoints."""
    endpoints = db.query(Endpoint).all()
    endpoint_statuses = []
    
    all_up = True
    all_down = True
    
    for endpoint in endpoints:
        # Get latest health check
        latest_check = (
            db.query(HealthCheck)
            .filter(HealthCheck.endpoint_id == endpoint.id)
            .order_by(HealthCheck.checked_at.desc())
            .first()
        )
        
        # Calculate 90-day uptime
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)
        total_checks = (
            db.query(HealthCheck)
            .filter(
                and_(
                    HealthCheck.endpoint_id == endpoint.id,
                    HealthCheck.checked_at >= ninety_days_ago,
                )
            )
            .count()
        )
        
        successful_checks = (
            db.query(HealthCheck)
            .filter(
                and_(
                    HealthCheck.endpoint_id == endpoint.id,
                    HealthCheck.checked_at >= ninety_days_ago,
                    HealthCheck.status == True,
                )
            )
            .count()
        )
        
        uptime_90d = (successful_checks / total_checks * 100) if total_checks > 0 else 0
        
        current_status = latest_check.status if latest_check else False
        
        if current_status:
            all_down = False
        else:
            all_up = False
        
        endpoint_statuses.append(
            EndpointStatus(
                endpoint=EndpointResponse(
                    id=endpoint.id,
                    name=endpoint.name,
                    url=endpoint.url,
                    method=endpoint.method,
                    headers=endpoint.headers,
                    body=endpoint.body,
                    expected_status=endpoint.expected_status,
                    created_at=endpoint.created_at,
                ),
                current_status=current_status,
                last_check=latest_check.checked_at if latest_check else None,
                response_time=latest_check.response_time if latest_check else None,
                uptime_90d=round(uptime_90d, 2),
            )
        )
    
    # Determine overall status
    if all_up:
        status = "operational"
        message = "All Systems Operational"
    elif all_down:
        status = "major_outage"
        message = "Major Outage"
    else:
        status = "partial_outage"
        message = "Partial System Outage"
    
    return OverallStatus(
        status=status,
        message=message,
        endpoints=endpoint_statuses,
    )


@app.get("/api/endpoints/{endpoint_id}/history", response_model=EndpointHistory)
async def get_endpoint_history(endpoint_id: int, db: Session = Depends(get_db)):
    """Get 90-day uptime history for a specific endpoint."""
    endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    daily_uptimes = []
    today = datetime.utcnow().date()
    
    for i in range(90):
        date = today - timedelta(days=i)
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())
        
        checks = (
            db.query(HealthCheck)
            .filter(
                and_(
                    HealthCheck.endpoint_id == endpoint_id,
                    HealthCheck.checked_at >= start_of_day,
                    HealthCheck.checked_at <= end_of_day,
                )
            )
            .all()
        )
        
        total = len(checks)
        successful = sum(1 for c in checks if c.status)
        uptime = (successful / total * 100) if total > 0 else -1  # -1 means no data
        
        daily_uptimes.append(
            DailyUptime(
                date=date.isoformat(),
                uptime_percentage=round(uptime, 2),
                total_checks=total,
                successful_checks=successful,
            )
        )
    
    return EndpointHistory(
        endpoint=EndpointResponse(
            id=endpoint.id,
            name=endpoint.name,
            url=endpoint.url,
            method=endpoint.method,
            headers=endpoint.headers,
            body=endpoint.body,
            expected_status=endpoint.expected_status,
            created_at=endpoint.created_at,
        ),
        daily_uptimes=list(reversed(daily_uptimes)),  # Oldest first
    )


@app.get("/api/endpoints/{endpoint_id}/checks", response_model=List[HealthCheckResponse])
async def get_recent_checks(
    endpoint_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get recent health checks for a specific endpoint."""
    endpoint = db.query(Endpoint).filter(Endpoint.id == endpoint_id).first()
    if not endpoint:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    
    checks = (
        db.query(HealthCheck)
        .filter(HealthCheck.endpoint_id == endpoint_id)
        .order_by(HealthCheck.checked_at.desc())
        .limit(limit)
        .all()
    )
    
    return checks


@app.post("/api/check-now")
async def trigger_health_check(db: Session = Depends(get_db)):
    """Manually trigger a health check for all endpoints."""
    await run_health_checks()
    return {"message": "Health checks triggered", "timestamp": datetime.utcnow().isoformat()}
