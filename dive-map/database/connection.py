import psycopg2
import json

def get_db():
    with open("config/settings.json") as f:
        cfg = json.load(f)

    return psycopg2.connect(
        dbname=cfg["db_name"],
        user=cfg["db_user"],
        password=cfg["db_pass"],
        host=cfg["db_host"],
        port=cfg["db_port"]
    )