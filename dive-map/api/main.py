from fastapi import FastAPI
from api.models import Dive
from api.ingest import insert_dive

app = FastAPI()

@app.post("/ingest")
def ingest(dive: Dive):
    insert_dive(dive)
    return {"status": "ok", "dive_id": dive.dive_id}