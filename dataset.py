import os

from tqdm import tqdm
import json
import botconfig

def is_valid_message(message: str) -> bool:
    """Filter out low-quality messages that harm model accuracy."""
    if not message or "```" in message:
        return False
    
    # Remove messages that are too short (likely noise)
    word_count = len(message.split())
    if word_count < botconfig.MIN_MESSAGE_LENGTH:
        return False
    
    # Skip messages that are mostly URLs or mentions
    if message.count("http") > 3 or message.count("@") > 3:
        return False
    
    # Skip messages with excessive emoji or special characters
    special_char_ratio = sum(1 for c in message if ord(c) > 127) / len(message)
    if special_char_ratio > 0.3:
        return False
    
    return True

def main() -> None:
    message_count = 0
    filtered_count = 0
    
    with open("data/messages.txt", "w", encoding="utf-8") as output_file:
        for root, _, files in os.walk("Messages"):
            for file in tqdm(files, desc=f"Iterating over {len(files)} files...", unit="file"):
                if file == "messages.json":
                    file_path = os.path.join(root, file)
                    print(f"\nProcessing: {file_path}")
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            dataset = json.load(f)
                            for entry in dataset:
                                message: str = entry.get("Contents", "") or ""
                                message = message.rstrip()
                                message_count += 1
                                
                                if is_valid_message(message):
                                    output_file.write(message + "\n")
                                else:
                                    filtered_count += 1
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Error reading {file_path}: {e}")
                        continue
    
    print(f"\nProcessing complete!")
    print(f"Total messages: {message_count}")
    print(f"Filtered out: {filtered_count}")
    print(f"Kept messages: {message_count - filtered_count}")

if __name__ == "__main__":
    main()
