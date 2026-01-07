from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EndpointBase(BaseModel):
    name: str
    url: str
    method: str = "GET"
    headers: Optional[str] = None
    body: Optional[str] = None
    expected_status: int = 200


class EndpointCreate(EndpointBase):
    pass


class EndpointResponse(EndpointBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class HealthCheckResponse(BaseModel):
    id: int
    endpoint_id: int
    status: bool
    response_time: Optional[float]
    status_code: Optional[int]
    error_message: Optional[str]
    checked_at: datetime

    class Config:
        from_attributes = True


class EndpointStatus(BaseModel):
    endpoint: EndpointResponse
    current_status: bool
    last_check: Optional[datetime]
    response_time: Optional[float]
    uptime_90d: float  # percentage


class DailyUptime(BaseModel):
    date: str
    uptime_percentage: float
    total_checks: int
    successful_checks: int


class EndpointHistory(BaseModel):
    endpoint: EndpointResponse
    daily_uptimes: List[DailyUptime]


class OverallStatus(BaseModel):
    status: str  # "operational", "partial_outage", "major_outage"
    message: str
    endpoints: List[EndpointStatus]
