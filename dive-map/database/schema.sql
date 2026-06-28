CREATE TABLE dives (
    id UUID PRIMARY KEY,
    user_id UUID,
    device_brand TEXT,
    device_model TEXT,
    timestamp_start TIMESTAMPTZ,
    timestamp_end TIMESTAMPTZ,
    site TEXT,
    gps GEOGRAPHY(POINT),
    max_depth_m FLOAT,
    avg_depth_m FLOAT,
    bottom_time_s INT,
    total_time_s INT,
    water_temp_c FLOAT
);

CREATE TABLE dive_profile (
    id SERIAL PRIMARY KEY,
    dive_id UUID REFERENCES dives(id) ON DELETE CASCADE,
    t INT,
    depth_m FLOAT,
    temp_c FLOAT,
    ndl FLOAT,
    ascent_rate_mpm FLOAT
);