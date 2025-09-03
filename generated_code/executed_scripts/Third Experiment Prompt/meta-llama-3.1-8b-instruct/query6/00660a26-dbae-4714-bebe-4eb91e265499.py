import csv
import os
import datetime
import json

# Define the root directory variable
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except FileNotFoundError as e:
    print(e)
    exit(1)

# Initialize the output CSV file
output_csv = os.path.join("query_responses", "results.csv")

# Initialize the CSV writer
with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])

    # Iterate over the 'your_instagram_activity' directory
    for dir_name in os.listdir(root_dir):
        if dir_name == "your_instagram_activity":
            # Iterate over the 'likes' and 'saved' subdirectories
            for sub_dir_name in os.listdir(os.path.join(root_dir, dir_name)):
                if sub_dir_name in ["likes", "saved"]:
                    # Get the JSON file path
                    json_file_path = os.path.join(root_dir, dir_name, sub_dir_name, "liked_posts.json" if sub_dir_name == "likes" else "saved_posts.json")

                    # Check if the JSON file exists
                    if not os.path.exists(json_file_path):
                        continue

                    # Load the JSON file
                    try:
                        with open(json_file_path, "r") as json_file:
                            json_data = json.load(json_file)
                    except json.JSONDecodeError as e:
                        print(f"Error: Failed to parse JSON file at {json_file_path}: {e}")
                        continue

                    # Check if the 'structure' key exists in the JSON data
                    if "structure" not in json_data:
                        print(f"Warning: The JSON file at {json_file_path} does not contain the 'structure' key.")
                        continue

                    # Iterate over the 'likes_media_likes' or 'saved_saved_media' list
                    for item in json_data["structure"][sub_dir_name]:
                        # Get the 'title' and 'string_list_data' or 'string_map_data' values
                        title = item.get("title", "")
                        data = item.get("string_list_data" if sub_dir_name == "likes" else "string_map_data", {})

                        # Iterate over the 'string_list_data' or 'string_map_data' dictionary
                        for key, value in data.items():
                            # Get the 'href' and 'timestamp' values
                            href = value.get("href", "")
                            timestamp = value.get("timestamp", 0)

                            # Get the 'Changed', 'New Value', and 'Change Date' values
                            changed = title
                            new_value = href
                            change_date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

                            # Write the row to the output CSV file
                            writer.writerow([changed, new_value, change_date])