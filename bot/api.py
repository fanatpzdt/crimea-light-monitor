from fastapi import FastAPI
from bot.database import (
    get_all_statuses,
    create_city_status_table
)


app = FastAPI()


# создаём таблицу при запуске API
create_city_status_table()


@app.get("/")
def home():

    return {
        "status": "ok",
        "service": "Crimea Light API"
    }


@app.get("/status")
def status():

    try:
        data = get_all_statuses()

        return {
            "ok": True,
            "data": data
        }

    except Exception as e:

        return {
            "ok": False,
            "error": str(e)
        }
