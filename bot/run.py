import asyncio
import threading
import uvicorn

from main import main as bot_main
from api import app


def start_api():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )


api_thread = threading.Thread(
    target=start_api
)

api_thread.start()


bot_main()
