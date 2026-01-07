from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func
from .database import Base


class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    url = Column(String)
    method = Column(String, default="GET")
    headers = Column(String, nullable=True)  # JSON string
    body = Column(String, nullable=True)  # JSON string
    expected_status = Column(Integer, default=200)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HealthCheck(Base):
    __tablename__ = "health_checks"

    id = Column(Integer, primary_key=True, index=True)
    endpoint_id = Column(Integer, index=True)
    status = Column(Boolean)  # True = up, False = down
    response_time = Column(Float, nullable=True)  # in milliseconds
    status_code = Column(Integer, nullable=True)
    error_message = Column(String, nullable=True)
    checked_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
