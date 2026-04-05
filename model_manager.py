import logging

import markovify

import botconfig as botconfig


def save_model(state_size: int) -> None:
    with open("data/messages.txt", encoding="utf-8") as f:
        text: str = f.read()

        text_model = markovify.NewlineText(
            text, well_formed=False, state_size=state_size)
        text_model.compile(inplace=True)
        model_json: str = text_model.to_json()
        with open("data/markov_model.json", "w", encoding="utf-8") as model_file:
            model_file.write(model_json)


def load_model() -> markovify.NewlineText:
    with open("data/markov_model.json", "r", encoding="utf-8") as model_file:
        model_json: str = model_file.read()
        return markovify.NewlineText.from_json(model_json)


def build_markov_model() -> markovify.NewlineText:
    logging.info("Loading messages.txt...")
    with open("data/messages.txt", encoding="utf-8") as f:
        text: str = f.read()

    logging.info("Creating NewlineText. This may take a while")
    return markovify.NewlineText(text, well_formed=False, state_size=botconfig.STATE_SIZE)
