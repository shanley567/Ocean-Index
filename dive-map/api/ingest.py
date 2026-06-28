from database.connection import get_db

def insert_dive(dive):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO dives (
            id, device_brand, device_model,
            timestamp_start, timestamp_end,
            site, gps,
            max_depth_m, avg_depth_m,
            bottom_time_s, total_time_s, water_temp_c
        ) VALUES (
            %s, %s, %s,
            %s, %s,
            %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326),
            %s, %s,
            %s, %s, %s
        )
    """, (
        dive.dive_id,
        dive.device["brand"],
        dive.device["model"],
        dive.timestamp_start,
        dive.timestamp_end,
        dive.location["site"],
        dive.location["gps"]["lon"],
        dive.location["gps"]["lat"],
        dive.summary.get("max_depth_m"),
        dive.summary.get("avg_depth_m"),
        dive.summary.get("bottom_time_s"),
        dive.summary.get("total_time_s"),
        dive.summary.get("water_temp_c")
    ))

    for sample in dive.profile["samples"]:
        cur.execute("""
            INSERT INTO dive_profile (
                dive_id, t, depth_m, temp_c, ndl, ascent_rate_mpm
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            dive.dive_id,
            sample["t"],
            sample["depth_m"],
            sample["temp_c"],
            sample.get("ndl"),
            sample.get("ascent_rate_mpm")
        ))

    conn.commit()
    cur.close()
    conn.close()
