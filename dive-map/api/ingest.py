# api/ingest.py

from datetime import timedelta
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from psycopg import connect
from psycopg.rows import dict_row

from api.models import DiveIngest
from database.connection import get_connection  # assumes you already have this


router = APIRouter()


@router.post("/ingest")
def ingest_dive(payload: DiveIngest):
    """
    Ingest a unified dive JSON into PostgreSQL:
    - dives table: one row per dive
    - dive_samples table: one row per profile sample
    """

    # Decide project-level dive_id
    dive_id = payload.dive_id or uuid4()

    try:
        with get_connection() as conn:
            conn.row_factory = dict_row

            with conn.cursor() as cur:
                # Insert dive metadata
                cur.execute(
                    """
                    INSERT INTO dives (
                        id,
                        device_dive_id,
                        device,
                        location,
                        summary,
                        timestamp_start,
                        timestamp_end
                    )
                    VALUES (
                        %s, %s, %s::jsonb, %s::jsonb, %s::jsonb, %s, %s
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        device_dive_id = EXCLUDED.device_dive_id,
                        device = EXCLUDED.device,
                        location = EXCLUDED.location,
                        summary = EXCLUDED.summary,
                        timestamp_start = EXCLUDED.timestamp_start,
                        timestamp_end = EXCLUDED.timestamp_end
                    """,
                    (
                        str(dive_id),
                        payload.device_dive_id,
                        payload.device.model_dump_json(),
                        payload.location.model_dump_json(),
                        payload.summary.model_dump_json(),
                        payload.timestamp_start,
                        payload.timestamp_end,
                    ),
                )

                # Insert samples
                base_ts = payload.timestamp_start

                for idx, sample in enumerate(payload.profile.samples):
                    sample_ts = base_ts + timedelta(seconds=sample.t)

                    cur.execute(
                        """
                        INSERT INTO dive_samples (
                            dive_id,
                            timestamp,
                            depth,
                            temperature,
                            device_sample_index,
                            raw
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s::jsonb
                        )
                        """,
                        (
                            str(dive_id),
                            sample_ts,
                            sample.depth_m,
                            sample.temp_c,
                            idx,
                            sample.model_dump_json(),
                        ),
                    )

            conn.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    return {"status": "ok", "dive_id": str(dive_id)}
