# Token for the bot, not to be confused with the account token
import os

TOKEN = os.environ.get("MARKOVBOT_TOKEN", "")
BOT_CHANNEL = int(os.environ.get("MARKOVBOT_CHANNEL_ID", 0))

# Performance and accuracy settings
TRY_COUNT = 25  # Reduced from 50 - we'll have better generation now
STATE_SIZE = 4  # Increased from 3 for better coherence
MAX_OVERLAP_RATIO = 0.7  # Prevent repetition of input sequences
SENTENCE_ATTEMPTS = 10  # Attempts per sentence generation
MIN_MESSAGE_LENGTH = 5  # Minimum words to keep in training data
