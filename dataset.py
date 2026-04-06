import os

from tqdm import tqdm
import json

def main() -> None:
    with open("data/messages.txt", "w", encoding="utf-8") as output_file:
        for root, _, files in os.walk("Messages"):
            for file in tqdm(files, desc=f"Iterating over {len(files)} files...", unit="file"):
                if file == "messages.json":
                    file_path = os.path.join(root, file)
                    print(f"\nDoing file: {file_path}")
                    with open(file_path, "r", encoding="utf-8") as f:
                        dataset = json.load(f)
                        for entry in dataset:
                            message: str = entry["Contents"] or ""
                            if "```" in message or message == "":
                                continue
                            output_file.write(message.rstrip() + "\n")

if __name__ == "__main__":
    main()
