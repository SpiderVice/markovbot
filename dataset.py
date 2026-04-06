import os
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import botconfig

def is_valid_message(message: str) -> bool:
    """Filter out low-quality messages that harm model accuracy."""
    if not message or "```" in message:
        return False
    
    word_count = len(message.split())
    if word_count < botconfig.MIN_MESSAGE_LENGTH:
        return False
    
    if message.count("http") > 3 or message.count("@") > 3:
        return False
    
    special_char_ratio = sum(1 for c in message if ord(c) > 127) / len(message)
    if special_char_ratio > 0.3:
        return False
    
    return True

def process_json_file(file_path: str) -> list[str]:
    """Process a single JSON file and return valid messages."""
    valid_messages = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)
            for entry in dataset:
                message: str = entry.get("Contents", "") or ""
                message = message.rstrip()
                if is_valid_message(message):
                    valid_messages.append(message)
    except (json.JSONDecodeError, KeyError) as e:
        logging.error(f"Error reading {file_path}: {e}")
    return valid_messages

def main() -> None:
    # Collect all JSON file paths
    json_files = []
    for root, _, files in os.walk("Messages"):
        for file in files:
            if file == "messages.json":
                json_files.append(os.path.join(root, file))
    
    print(f"Found {len(json_files)} JSON files to process")
    
    message_count = 0
    filtered_count = 0
    
    with open("data/messages.txt", "w", encoding="utf-8") as output_file:
        # Process files in parallel (4-8 threads recommended)
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(process_json_file, f): f for f in json_files}
            for future in tqdm(as_completed(futures), total=len(json_files), desc="Processing files"):
                try:
                    messages = future.result()
                    for message in messages:
                        output_file.write(message + "\n")
                        message_count += 1
                except Exception as e:
                    logging.error(f"Error processing file: {e}")
    
    print(f"\nProcessing complete!")
    print(f"Total messages processed: {message_count}")

if __name__ == "__main__":
    main()
