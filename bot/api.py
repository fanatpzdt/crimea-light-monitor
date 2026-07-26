from fastapi import FastAPI
from bot.database import get_all_statuses


app = FastAPI(
    title="Crimea Light API"
)


@app.get("/status")
def status():

    return get_all_statuses()


@app.get("/")
def home():

    return {
        "status": "ok",
        "service": "Crimea Light API"
    }
