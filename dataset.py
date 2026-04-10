import os

from loguru import logger
from tqdm import tqdm
import json

messages: list[str] = []


def twitter() -> None:
    with open("tweets.js", "r", encoding="utf-8") as f:
        data: str = f.read()
        json_data: str = data.replace(
            "window.YTD.tweets.part0 = ", "").rstrip(";")

        tweets = json.loads(json_data)

        for tweet_entry in tqdm(tweets, desc=f"Iterating over {len(tweets)} tweets...", unit="tweet"):
            tweet = tweet_entry.get("tweet", {})
            message: str = tweet.get("full_text", "") or ""
            if message != "" and not message.startswith("RT "):
                messages.append(message)

    with open("tweets.txt", "w", encoding="utf-8") as f:
        if messages != []:
            for message in tqdm(messages, desc="Writing tweets to file"):
                message = message.rstrip()
                if "\n\n" in message:
                    message = message.replace("\n\n", "\n")
                if message != "":
                    f.write(message + "\n")
        else:
            raise ValueError(
                "You must have a non-empty list of messages in order for markovbot to work.")


def discord() -> None:
    for root, _, files in os.walk("Messages"):
        for file in tqdm(files, desc=f"Iterating over {len(files)} files...", unit="file"):
            if file == "messages.json":
                file_path = os.path.join(root, file)
                logger.info(f"\nDoing file: {file_path}")
                with open(file_path, "r", encoding="utf-8") as f:
                    dataset = json.load(f)
                    for entry in dataset:
                        message: str = entry["Contents"] or ""
                        # Let's skip code blocks and quotes, it may end up confusing the model.
                        if "```" in message:
                            continue
                        if message != "":
                            messages.append(message)

    with open("discord_messages.txt", "w", encoding="utf-8") as f:
        if messages != []:
            for message in tqdm(messages, desc="Writing messages to file"):
                message = message.rstrip()
                if message != "":
                    f.write(message + "\n")
        else:
            raise ValueError(
                "You must have a non-empty list of messages in order for markovbot to work.")


def join() -> None:
    try:
        with open("discord_messages.txt", "r", encoding="utf-8") as f:
            logger.info("Opened discord_messages.txt...")
            with open("tweets.txt", "r", encoding="utf-8") as g:
                logger.info("Opened tweets.txt...")
                discord_content: str = f.read()
                twitter_content: str = g.read()
                final_content: str = discord_content + twitter_content
                logger.info("Writing final messages.txt file")
                with open("messages.txt", "w", encoding="utf-8") as ff:
                    ff.write(final_content)
    except FileNotFoundError as e:
        logger.error(f"There's a file missing... {repr(e)}")


if __name__ == "__main__":
    discord()
    twitter()
    join()
