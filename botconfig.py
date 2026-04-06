import os
# Token for the bot, not to be confused with the account token
TOKEN = os.environ.get("MARKOVBOT_TOKEN", "") 
BOT_CHANNEL = int(os.environ.get("MARKOVBOT_CHANNEL_ID", 0))

TRY_COUNT = int(os.environ.get("TRY_COUNT", 50))
STATE_SIZE = int(os.environ.get("STATE_SIZE", 3))

