from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class PlanningStrategy(str, Enum):
    fastest = "fastest"
    shortest = "shortest"


class CityStatus(str, Enum):
    success = 'success'
    failed = 'failed'
    updated = 'updated'
    deleted = 'deleted'


class RouteRequest(BaseModel):
    start: str
    destination: str
    strategy: PlanningStrategy


class RouteResponse(BaseModel):
    distance_km: float
    duration_minutes: float
    route: List[str]


class City(BaseModel):
    name: str
    # negative values stands for souther hemisphere
    lattitude: float = Field(..., ge=-90, le=90)
    # negative values stands for western hemisphere
    longitude: float = Field(..., ge=-180, le=180)


class CityResponse(BaseModel):
    status: CityStatus


class Road(BaseModel):
    first_city_name: str
    second_city_name: str
    distance_km: float = Field(..., gt=0)
    duration_minutes: float = Field(..., gt=0)
