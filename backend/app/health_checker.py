import httpx
import json
import time
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Endpoint, HealthCheck
from .database import SessionLocal
import asyncio


async def check_endpoint(endpoint: Endpoint) -> dict:
    """Check if an endpoint is healthy."""
    start_time = time.time()
    result = {
        "endpoint_id": endpoint.id,
        "status": False,
        "response_time": None,
        "status_code": None,
        "error_message": None,
    }

    try:
        headers = json.loads(endpoint.headers) if endpoint.headers else {}
        body = json.loads(endpoint.body) if endpoint.body else None

        async with httpx.AsyncClient(timeout=30.0) as client:
            if endpoint.method.upper() == "GET":
                response = await client.get(endpoint.url, headers=headers)
            elif endpoint.method.upper() == "POST":
                response = await client.post(
                    endpoint.url,
                    headers=headers,
                    json=body if body else None,
                )
            else:
                response = await client.request(
                    endpoint.method.upper(),
                    endpoint.url,
                    headers=headers,
                    json=body if body else None,
                )

        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to ms

        result["response_time"] = round(response_time, 2)
        result["status_code"] = response.status_code
        
        # Consider 2xx and 3xx status codes as success
        if 200 <= response.status_code < 400:
            result["status"] = True
        else:
            result["status"] = False
            result["error_message"] = f"HTTP {response.status_code}"

    except httpx.TimeoutException:
        result["error_message"] = "Request timed out"
    except httpx.ConnectError:
        result["error_message"] = "Connection failed"
    except Exception as e:
        result["error_message"] = str(e)[:200]

    return result


async def run_health_checks():
    """Run health checks for all endpoints."""
    db = SessionLocal()
    try:
        endpoints = db.query(Endpoint).all()
        
        for endpoint in endpoints:
            result = await check_endpoint(endpoint)
            
            health_check = HealthCheck(
                endpoint_id=result["endpoint_id"],
                status=result["status"],
                response_time=result["response_time"],
                status_code=result["status_code"],
                error_message=result["error_message"],
                checked_at=datetime.utcnow(),
            )
            db.add(health_check)
        
        db.commit()
        print(f"[{datetime.utcnow()}] Health checks completed for {len(endpoints)} endpoints")
    except Exception as e:
        print(f"Error running health checks: {e}")
        db.rollback()
    finally:
        db.close()


def sync_run_health_checks():
    """Synchronous wrapper for the health checker."""
    asyncio.run(run_health_checks())
