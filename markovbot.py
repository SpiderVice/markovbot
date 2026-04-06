
import discord
import markovify
import logging
import os
import asyncio
import time

import utils
import botconfig
import model_manager

# You may not want to log it to a file, fyi
handler = logging.FileHandler(
    filename='logs/discord.log', encoding='utf-8', mode='w')


def try_load_model() -> markovify.NewlineText:
    if not os.path.exists("data/markov_model.json"):
        logging.info(
            "markov_model.json not found. Loading messages.txt and creating model...")
        text_model: markovify.NewlineText = model_manager.build_markov_model()
        logging.info("Saving model to markov_model.json...")
        model_manager.save_model(botconfig.STATE_SIZE)
        return text_model
    else:
        logging.info("markov_model.json found. Loading model...")
        return model_manager.load_model()


text_model: markovify.NewlineText = try_load_model()
text_model.compile(inplace=True)  # Compile the model for faster generation


def random_with_lookup(look_up_term: str) -> str:
    """
    Generate a message containing the lookup term.
    Optimized for performance with early exit and efficient string matching.
    """
    final_message = ""
    logging.info(f"Generating message with lookup term: {look_up_term}")
    
    look_up_lower = look_up_term.lower()
    attempt_count = 0
    start_time = time.time()
    
    # Early exit: cap attempts at TRY_COUNT * SENTENCE_ATTEMPTS
    max_total_attempts = botconfig.TRY_COUNT * botconfig.SENTENCE_ATTEMPTS
    
    while attempt_count < max_total_attempts and not final_message:
        # Generate a single sentence with improved parameters
        generated_message: str = text_model.make_sentence(
            tries=botconfig.SENTENCE_ATTEMPTS,
            max_overlap_ratio=botconfig.MAX_OVERLAP_RATIO
        )
        
        if generated_message and look_up_lower in generated_message.lower():
            final_message = generated_message
            break
        
        attempt_count += 1
    
    # Format output with timing information
    elapsed_time = time.time() - start_time
    if final_message:
        final_message += f"\n\n*Generated in {attempt_count} attempts ({elapsed_time:.2f}s)*"
        logging.info(f"Success: {attempt_count} attempts in {elapsed_time:.2f}s")
    else:
        final_message = f"Could not generate a message containing '{look_up_term}' after {max_total_attempts} attempts."
        logging.warning(f"Failed after {max_total_attempts} attempts in {elapsed_time:.2f}s")
    
    return final_message


def make_random_sentence() -> str:
    """Generate a random sentence from the model."""
    try:
        sentence = text_model.make_sentence(
            tries=botconfig.SENTENCE_ATTEMPTS,
            max_overlap_ratio=botconfig.MAX_OVERLAP_RATIO
        )
        return sentence or "I couldn't generate a sentence. Try again!"
    except Exception as e:
        logging.error(f"Error generating sentence: {e}")
        return "An error occurred while generating a message."


# Client code

client: discord.Client = utils.load_discord_client()


async def status_check() -> None:
    bot_channel = client.get_channel(botconfig.BOT_CHANNEL)
    if bot_channel and isinstance(bot_channel, discord.TextChannel):
        await bot_channel.send(
            f"## [MARKOVBOT] The bot is now **online**!\n"
            f"### Settings: STATE_SIZE={botconfig.STATE_SIZE}, "
            f"TRY_COUNT={botconfig.TRY_COUNT}, "
            f"MAX_OVERLAP_RATIO={botconfig.MAX_OVERLAP_RATIO}"
        )


@client.event
async def on_ready() -> None:
    logging.info(f"Logged in as {client.user}")
    await status_check()


@client.event
async def on_message(message: discord.Message) -> None:
    logging.info(f"Message received from {message.author}.")

    if message.content == "" or message.author == client.user or not message.content.startswith("!"):
        return

    if not utils.is_valid_channel(message):
        return

    split_message: list[str] = message.content.rstrip().split(" ")
    cmd: str = split_message[0] or ""
    terms: list[str] = split_message[1:] if len(split_message) > 1 else []
    terms_str: str = " ".join(terms)

    if cmd not in ["!talk", "!randomtalk"]:
        logging.info(
            f"Message does not start with a recognized command. Message content: {message.content}")
        await message.channel.send(f"OOC: Unrecognized command {cmd}. Please use !talk or !randomtalk followed by a term to generate a message.")
        return  # Not sure why I need this return

    isTalk: bool = cmd == "!talk"
    isRandomTalk: bool = cmd == "!randomtalk"
    generated_response = ""

    try:
        if len(terms) > botconfig.STATE_SIZE - 1:
            await message.channel.send(f"OOC: You cannot have more than {botconfig.STATE_SIZE - 1} words after the {cmd} command. Try again!")
            return

        if isTalk:
            # Generate sentence starting with the given term(s)
            start_time = time.time()
            generated_response: str = text_model.make_sentence_with_start(
                terms_str, 
                tries=botconfig.SENTENCE_ATTEMPTS * 3,  # More tries for exact start matching
                max_overlap_ratio=botconfig.MAX_OVERLAP_RATIO
            ) or f"OOC: I tried to start with '{terms_str}' but couldn't generate a valid sentence. Try another term!"
            
            elapsed = time.time() - start_time
            if generated_response and "OOC" not in generated_response:
                generated_response += f"\n\n*Generated in {elapsed:.2f}s*"
                
        elif isRandomTalk:
            # Generate random sentence containing the term
            if not terms_str:
                generated_response = await asyncio.to_thread(make_random_sentence)
            else:
                generated_response = await asyncio.to_thread(random_with_lookup, terms_str)
        else:
            generated_response = "OOC: Unrecognized command. Please use !talk or !randomtalk followed by a term to generate a message."
            
    except Exception as e:
        logging.error(f"Error generating message: {e}", exc_info=True)
        generated_response = f"OOC: An error occurred while generating the message: {type(e).__name__}."

    if not generated_response or generated_response == "":
        generated_response = f"OOC: I couldn't generate a message with the term '{terms_str}'. Try another term?"

    await message.channel.send(generated_response)


client.run(botconfig.TOKEN, log_handler=handler, root_logger=True)
