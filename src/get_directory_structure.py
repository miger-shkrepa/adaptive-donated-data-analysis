import os
import json

# Global registry for unique structures
unique_structures = set()

# Extracts the structure of a JSON object, capturing unique examples of objects and arrays.
def extract_json_structure(data):
    if isinstance(data, dict):
        structure = {key: extract_json_structure(value) for key, value in data.items()}
        return structure

    elif isinstance(data, list):
        # For lists, analyze all unique item structures
        unique_item_structures = set()
        for item in data:
            item_structure = json.dumps(extract_json_structure(item), sort_keys=True)
            unique_item_structures.add(item_structure)

        return [json.loads(structure) for structure in unique_item_structures]

    else:
        return type(data).__name__

# Analyzes the inbox folder and selects the conversation folder with the most unique message structures.
def analyze_inbox_structure(inbox_path):
    conversation_structure = None
    most_unique_count = 0

    for folder in os.listdir(inbox_path):
        folder_path = os.path.join(inbox_path, folder)
        if os.path.isdir(folder_path):
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if item.endswith('.json'):
                    try:
                        with open(item_path, 'r', encoding='utf-8') as json_file:
                            json_content = json.load(json_file)
                            if "messages" in json_content:
                                # Extract unique message structures
                                message_structures = set()
                                for message in json_content["messages"]:
                                    structure = json.dumps(extract_json_structure(message), sort_keys=True)
                                    message_structures.add(structure)

                                # Compare uniqueness
                                if len(message_structures) > most_unique_count:
                                    most_unique_count = len(message_structures)
                                    conversation_structure = {
                                        "username_placeholder": {
                                            item: {
                                                "type": "json",
                                                "structure": extract_json_structure(json_content)
                                            }
                                        }
                                    }
                    except Exception:
                        continue  # Skip invalid JSON files

    return conversation_structure

# Recursively records the directory structure into a nested dictionary (Special handling for .jpg files and the inbox folder).
def record_directory_structure(directory_path):
    directory_structure = {}

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)

        if os.path.isdir(item_path):
            if item.lower() == "inbox":
                # Special handling for the inbox folder
                directory_structure[item] = analyze_inbox_structure(item_path)
            else:
                directory_structure[item] = record_directory_structure(item_path)

        elif os.path.isfile(item_path):
            if item.endswith('.json'):
                try:
                    with open(item_path, 'r', encoding='utf-8') as json_file:
                        json_content = json.load(json_file)
                        json_structure = extract_json_structure(json_content)
                        directory_structure[item] = {"type": "json", "structure": json_structure}
                except Exception:
                    directory_structure[item] = {"type": "json", "error": "Invalid or unreadable JSON"}
            elif item.endswith('.jpg'):
                # Rename all .jpg files to "image.jpg"
                directory_structure["image.jpg"] = None
            else:
                directory_structure[item] = None

    return directory_structure

# Saves the directory structure to a TXT file.
def save_structure_to_files(structure, txt_file):
    with open(txt_file, 'w', encoding='utf-8') as txt_out:
        txt_out.write(json.dumps(structure, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    # Replace 'main_directory_path' with the actual path to your main directory
    main_directory_path = "C:/Users/Miger Shkrepa/Downloads/instagram-leridash-2025-04-15-tyc7Gjjv"
    txt_output_file = "../data/directory_structure_final2.txt"

    if os.path.exists(main_directory_path) and os.path.isdir(main_directory_path):
        structure = record_directory_structure(main_directory_path)

        # Save to both JSON and TXT files
        save_structure_to_files(structure, txt_output_file)
        print(f"Directory structure has been saved to {txt_output_file}")
    else:
        print("Invalid directory path. Please provide a valid path.")