import csv
import json
import uuid

def safe_float(value):
    try:
        return float(value)
    except ValueError:
        if "*" in value:
            a, b = value.split("*")
            return float(a) * float(b)
        raise

def parse_garmin_csv(path):
    dive = {
        "dive_id": str(uuid.uuid4()),
        "device": {
            "brand": "Garmin",
            "model": "Descent Mk2"
        },
        "location": {},
        "summary": {},
        "profile": {
            "interval_s": 5,
            "samples": []
        }
    }

    with open(path, "r") as f:
        reader = csv.reader(f)

        for row in reader:

            # Skip empty lines
            if not row:
                continue

            # Skip comment lines
            if row[0].startswith("#"):
                continue

            # Skip header rows inside message blocks
            if row[0] in ["FileId", "DeviceInfo", "DiveSummary", "Record"] and \
               row[1] in ["Timestamp", "StartTime", "EndTime", "BatteryStatus", "WaterTemperature"]:
                continue

            # -----------------------------
            # FILE ID BLOCK
            # -----------------------------
            if row[0] == "FileId":
                dive["timestamp_start"] = row[5]

            # -----------------------------
            # DIVE SUMMARY BLOCK
            # -----------------------------
            elif row[0] == "DiveSummary":
                dive["timestamp_end"] = row[3]
                dive["summary"]["max_depth_m"] = safe_float(row[4])
                dive["summary"]["avg_depth_m"] = safe_float(row[5])
                dive["summary"]["bottom_time_s"] = safe_float(row[6])
                dive["summary"]["total_time_s"] = safe_float(row[7])
                dive["summary"]["water_temp_c"] = safe_float(row[8])

                dive["location"] = {
                    "site": row[11],
                    "gps": {
                        "lat": safe_float(row[12]),
                        "lon": safe_float(row[13])
                    }
                }

            # -----------------------------
            # PROFILE RECORD BLOCK
            # -----------------------------
            elif row[0] == "Record":
                dive["profile"]["samples"].append({
                    "t": len(dive["profile"]["samples"]) * 5,
                    "depth_m": safe_float(row[2]),
                    "temp_c": safe_float(row[3]),
                    "ascent_rate_mpm": safe_float(row[4]),
                    "ndl": safe_float(row[5])
                })

    return dive


if __name__ == "__main__":
    dive = parse_garmin_csv("examples/garmin_dive_01.fit.csv")

    with open("output/unified_dive_01.json", "w") as f:
        json.dump(dive, f, indent=2)

    print("✔ Garmin dive converted → unified JSON")
