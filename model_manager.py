from loguru import logger
import os
import json

import markovify

import botconfig


def save_model(state_size: int) -> None:
    with open("data/messages.txt", encoding="utf-8") as f:
        text: str = f.read()

        text_model = markovify.NewlineText(
            text, well_formed=False, state_size=state_size)
        text_model.compile(inplace=True)
        model_json: str = text_model.to_json()
        try:
            with open("data/markov_model.json", "w", encoding="utf-8") as model_file:
                model_file.write(model_json)

            save_model_metadata(state_size)
        except PermissionError as e:
            logger.error(
                f"Permission error while trying to save the model: {repr(e)}")
            logger.info(
                f"Permission is {os.access('data/markov_model.json', os.W_OK)}")


def save_model_metadata(state_size: int) -> None:
    metadata = {"state_size": state_size}
    try:
        with open("data/model_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f)
    except PermissionError as e:
        logger.error(
            f"Permission error while trying to save model metadata: {repr(e)}")


def get_saved_state_size() -> int | None:
    try:
        with open("data/model_metadata.json", "r", encoding="utf-8") as f:
            metadata = json.load(f)
            return metadata.get("state_size")
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, PermissionError) as e:
        logger.warning(
            f"Could not read model metadata: {repr(e)}")
        return None


def load_model() -> markovify.NewlineText:
    try:
        with open("data/markov_model.json", "r", encoding="utf-8") as model_file:
            model_json: str = model_file.read()
            return markovify.NewlineText.from_json(model_json)
    except FileNotFoundError:
        logger.error(
            "markov_model.json not found. Please build the model first.")
        raise
    except PermissionError as e:
        logger.error(
            f"Permission error while trying to load the model: {repr(e)}")
        logger.info(
            f"Permission is {os.access('data/markov_model.json', os.R_OK)}")
        raise


def should_rebuild_model() -> bool:
    saved_state_size = get_saved_state_size()
    if saved_state_size is None:
        return True  # No metadata found, regenerate
    if saved_state_size != botconfig.STATE_SIZE:
        logger.info(
            f"STATE_SIZE changed from {saved_state_size} to {botconfig.STATE_SIZE}. "
            "Regenerating model...")
        return True
    return False


def build_markov_model() -> markovify.NewlineText:
    logger.info("Loading messages.txt...")
    try:
        with open("data/messages.txt", encoding="utf-8") as f:
            text: str = f.read()
    except FileNotFoundError:
        logger.error(
            "messages.txt not found. Please run the dataset generation script first.")
        raise
    except PermissionError as e:
        logger.error(
            f"Permission error while trying to load messages.txt: {repr(e)}")
        logger.info(
            f"Permission is {os.access('data/messages.txt', os.R_OK)}")
        raise

    logger.info("Creating NewlineText. This may take a while")
    text_model = markovify.NewlineText(text, well_formed=False, state_size=botconfig.STATE_SIZE)
    # Save the model with the current STATE_SIZE
    save_model(botconfig.STATE_SIZE)
    return text_model
