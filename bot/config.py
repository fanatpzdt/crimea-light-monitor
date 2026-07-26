import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ID канала (например -1001234567890)
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Через сколько подтверждений публиковать пост
ALERT_THRESHOLD = 3
