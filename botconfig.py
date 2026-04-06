# Token for the bot, not to be confused with the account token
import os

TOKEN = os.environ.get("MARKOVBOT_TOKEN", "")
BOT_CHANNEL = int(os.environ.get("MARKOVBOT_CHANNEL_ID", 0))

TRY_COUNT = int(os.environ.get("TRY_COUNT", 50))
STATE_SIZE = int(os.environ.get("STATE_SIZE", 3))
MAX_OVERLAP_RATIO = float(os.environ.get("MAX_OVERLAP_RATIO", 0.7))
