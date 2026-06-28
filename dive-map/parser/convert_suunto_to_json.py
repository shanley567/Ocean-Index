import xml.etree.ElementTree as ET
import json
import uuid

# Suunto DM5 namespace
NS = {"dm5": "http://www.suunto.com/dm5"}

def safe_float(value):
    try:
        return float(value)
    except ValueError:
        return None

def parse_suunto_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()

    # Find the <Dive> node
    dive_node = root.find("dm5:Dive", NS)
    if dive_node is None:
        raise ValueError("No <Dive> element found in XML.")

    # Build unified dive object
    dive = {
        "dive_id": str(uuid.uuid4()),
        "device": {
            "brand": "Suunto",
            "model": "Unknown"
        },
        "location": {},
        "summary": {},
        "profile": {
            "interval_s": 5,
            "samples": []
        }
    }

    # -----------------------------
    # BASIC FIELDS
    # -----------------------------
    date = dive_node.find("dm5:Date", NS).text
    time = dive_node.find("dm5:Time", NS).text
    dive["timestamp_start"] = f"{date}T{time}Z"
    dive["timestamp_end"] = dive["timestamp_start"]  # Suunto DM5 does not always include end time

    # -----------------------------
    # LOCATION
    # -----------------------------
    site = dive_node.find("dm5:Site", NS)
    gps = dive_node.find("dm5:GPS", NS)

    dive["location"] = {
        "site": site.text if site is not None else "Unknown",
        "gps": {
            "lat": safe_float(gps.find("dm5:Latitude", NS).text),
            "lon": safe_float(gps.find("dm5:Longitude", NS).text)
        }
    }

    # -----------------------------
    # SUMMARY
    # -----------------------------
    max_depth = dive_node.find("dm5:MaxDepth", NS)
    temp = dive_node.find("dm5:WaterTemperature", NS)

    dive["summary"]["max_depth_m"] = safe_float(max_depth.text)
    dive["summary"]["water_temp_c"] = safe_float(temp.text)
    dive["summary"]["avg_depth_m"] = None
    dive["summary"]["bottom_time_s"] = None
    dive["summary"]["total_time_s"] = None

    # -----------------------------
    # PROFILE SAMPLES
    # -----------------------------
    profile = dive_node.find("dm5:Profile", NS)
    if profile is not None:
        samples = profile.findall("dm5:Sample", NS)
        for sample in samples:
            t = safe_float(sample.find("dm5:TimeOffset", NS).text)
            depth = safe_float(sample.find("dm5:Depth", NS).text)
            temp = safe_float(sample.find("dm5:Temperature", NS).text)

            dive["profile"]["samples"].append({
                "t": t,
                "depth_m": depth,
                "temp_c": temp,
                "ndl": None,
                "ascent_rate_mpm": None
            })

    return dive


if __name__ == "__main__":
    dive = parse_suunto_xml("examples/suunto_dive_01.xml")

    with open("output/unified_suunto_dive_01.json", "w") as f:
        json.dump(dive, f, indent=2)

    print("✔ Suunto dive converted → unified JSON")
