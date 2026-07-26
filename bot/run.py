import threading
import uvicorn


from api import app


def start_api():

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080
    )


threading.Thread(
    target=start_api,
    daemon=True
).start()


bot_main()
