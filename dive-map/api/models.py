# api/models.py

from typing import Optional, List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class Device(BaseModel):
    brand: str
    model: str


class GPS(BaseModel):
    lat: float
    lon: float


class Location(BaseModel):
    site: str
    gps: GPS


class Summary(BaseModel):
    max_depth_m: float
    avg_depth_m: float
    bottom_time_s: float
    total_time_s: float
    water_temp_c: float


class ProfileSample(BaseModel):
    t: float                 # seconds from start
    depth_m: float
    temp_c: float
    ascent_rate_mpm: float
    ndl: float


class Profile(BaseModel):
    interval_s: float
    samples: List[ProfileSample]


class DiveIngest(BaseModel):
    # Imported from device/file (optional, for deduplication)
    device_dive_id: Optional[str] = None

    # Project-unique ID (optional; generated if missing)
    dive_id: Optional[UUID] = None

    device: Device
    location: Location
    summary: Summary
    profile: Profile

    timestamp_start: datetime
    timestamp_end: datetime
