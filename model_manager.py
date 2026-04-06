import logging
import os
import json

import markovify

import botconfig


def save_model(state_size: int) -> None:
    """Build and save markov model with improved accuracy settings."""
    with open("data/messages.txt", encoding="utf-8") as f:
        text: str = f.read()

        # Use well_formed=True for grammatically correct sentences
        text_model = markovify.NewlineText(
            text, 
            well_formed=True,  # Changed from False for better accuracy
            state_size=state_size
        )
        text_model.compile(inplace=True)

        # Use json.dump instead of to_json() + write
        with open("data/markov_model.json", "w", encoding="utf-8") as model_file:
            json.dump(text_model.to_json(), model_file)
        
        logging.info(f"Model saved with state_size={state_size}")


def load_model() -> markovify.NewlineText:
    """Load pre-compiled markov model."""
    try:
        with open("data/markov_model.json", "r", encoding="utf-8") as model_file:
            model_json = json.load(model_file)
            model = markovify.NewlineText.from_json(model_json)
            logging.info("Model loaded successfully")
            return model
    except FileNotFoundError:
        logging.error(
            "markov_model.json not found. Please build the model first.")
        raise
    except PermissionError as e:
        logging.error(
            f"Permission error while trying to load the model: {repr(e)}")
        logging.info(
            f"Permission is {os.access('data/markov_model.json', os.R_OK)}")
        raise


def build_markov_model() -> markovify.NewlineText:
    """Build a new markov model from messages.txt with optimized settings."""
    logging.info("Loading messages.txt...")
    try:
        with open("data/messages.txt", encoding="utf-8") as f:
            text: str = f.read()
    except FileNotFoundError:
        logging.error(
            "messages.txt not found. Please run the dataset generation script first.")
        raise
    except PermissionError as e:
        logging.error(
            f"Permission error while trying to load messages.txt: {repr(e)}")
        logging.info(
            f"Permission is {os.access('data/messages.txt', os.R_OK)}")
        raise

    logging.info(f"Creating NewlineText with state_size={botconfig.STATE_SIZE}. This may take a while...")
    
    # Build model with improved accuracy settings
    text_model = markovify.NewlineText(
        text, 
        well_formed=True,  # Only generate grammatically correct sentences
        state_size=botconfig.STATE_SIZE
    )
    
    logging.info("Model built successfully")
    return text_model
