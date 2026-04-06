# MarkovBot

## Requirements

- Have a Discord data dump copied to the root directory of this project. (Messages folder)
- Have run the dataset.py script to convert the JSON into a TXT which will be read by markovify.
- Have environment variables set for the Discord bot token and the target channel ID.
    1. `MARKOVBOT_TOKEN`: The token for your Discord bot.
    2. `MARKOVBOT_CHANNEL_ID`: The ID of the Discord channel where the bot will post messages.

## Usage (Locally)

### Install UV

#### Linux (Curl)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Linux (Wget)

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

#### Windows (Winget, Preferred)

```powershell
winget install --id=astral-sh.uv  -e
```

#### Windows (PowerShell)

> This bypasses the execution policy. Be sure that you understand the risks associated with this command before running it.

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Synchronize the environment

```bash
uv sync
```

### Run the bot

```bash
uv run markovbot.py
```

> Keep an eye on logs in case something goes wrong. Startup time may take up to 5 minutes, be patient and check the logs.

## Usage (Docker)

### Build the Docker image

```bash
docker build -t markovbot .
```

### Run the Docker container

```bash
docker run -d --name markovbot -e MARKOVBOT_TOKEN=your_token_here -e MARKOVBOT_CHANNEL_ID=your_channel_id_here markovbot
```

## Useful Tidbits

You can read more about Markovify at [Markovify - GitHub](https://github.com/jsvine/markovify)