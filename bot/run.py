import threading
import uvicorn

from main import main as bot_main
from api import app


def start_bot():
    bot_main()


def start_api():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )


threading.Thread(
    target=start_bot
).start()


start_api()
