-- schema/schema.sql

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Main dives table
CREATE TABLE IF NOT EXISTS dives (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,  -- project-unique dive_id
    device_dive_id TEXT,                            -- ID from device/file (optional)
    device JSONB,                                   -- device metadata (brand, model, etc.)
    location JSONB,                                 -- site + GPS
    summary JSONB,                                  -- max depth, avg depth, times, etc.
    timestamp_start TIMESTAMPTZ NOT NULL,
    timestamp_end TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Optional: prevent exact duplicate device_dive_id + timestamp_start
CREATE UNIQUE INDEX IF NOT EXISTS dives_device_unique
    ON dives (device_dive_id, timestamp_start)
    WHERE device_dive_id IS NOT NULL;

-- Samples table (per-interval profile)
CREATE TABLE IF NOT EXISTS dive_samples (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    dive_id UUID NOT NULL REFERENCES dives(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ NOT NULL,
    depth NUMERIC NOT NULL,
    temperature NUMERIC,
    device_sample_index INTEGER,
    raw JSONB
);

CREATE INDEX IF NOT EXISTS dive_samples_dive_id_idx
    ON dive_samples (dive_id, timestamp);
