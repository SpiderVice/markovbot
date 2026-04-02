# MarkovBot

## Requirements

- Have a Discord data dump copied to the root directory of this project. (Messages folder)
- Have run the dataset.py script to convert the JSON into a TXT which will be read by markovify.
- Have environment variables set for the Discord bot token and the target channel ID.
    1. `MARKOVBOT_TOKEN`: The token for your Discord bot.
    2. `MARKOVBOT_CHANNEL_ID`: The ID of the Discord channel where the bot will post messages.

## Usage

1. Create a python virtual environment and activate it.

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install the necessary packages.

```bash
pip install -r requirements.txt
```

3. Run the main script. (PS: Optionally attach it to a tmux instance for convenience)

```bash
python3 markovbot.py
```

> Keep an eye on logs in case something goes wrong. Startup time is about 1 minute or so, depends on the host.

## Useful

You can read more about Markovify at [Markovify - GitHub](https://github.com/jsvine/markovify)