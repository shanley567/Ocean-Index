from pydantic import BaseModel
from typing import List, Optional

class Sample(BaseModel):
    t: float
    depth_m: float
    temp_c: float
    ndl: Optional[float]
    ascent_rate_mpm: Optional[float]

class Dive(BaseModel):
    dive_id: str
    device: dict
    location: dict
    summary: dict
    profile: dict
    timestamp_start: str
    timestamp_end: str