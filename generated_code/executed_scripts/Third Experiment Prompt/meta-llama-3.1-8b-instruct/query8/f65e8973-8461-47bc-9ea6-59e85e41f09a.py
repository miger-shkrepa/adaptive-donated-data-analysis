import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the result dictionary
result = {"User": [], "Post Likes": [], "Story Likes": [], "Comments": []}

# Define the function to process the data
def process_data():
    # Iterate over the subdirectories
    for dir in os.listdir(root_dir):
        # Check if the subdirectory is a directory
        if os.path.isdir(os.path.join(root_dir, dir)):
            # Iterate over the files in the subdirectory
            for file in os.listdir(os.path.join(root_dir, dir)):
                # Check if the file is a JSON file
                if file.endswith(".json"):
                    # Open the JSON file
                    with open(os.path.join(root_dir, dir, file), "r") as f:
                        # Load the JSON data
                        data = json.load(f)
                        # Check if the data has the required structure
                        if "type" in data and data["type"] == "json":
                            # Process the data
                            process_json_data(data, result)

# Define the function to process the JSON data
def process_json_data(data, result):
    # Check if the data has the required structure
    if "structure" in data:
        # Iterate over the items in the structure
        for item in data["structure"]:
            # Check if the item is a list
            if isinstance(item, list):
                # Iterate over the items in the list
                for subitem in item:
                    # Check if the subitem has the required structure
                    if "string_list_data" in subitem:
                        # Process the string list data
                        process_string_list_data(subitem, result)
                    elif "media_list_data" in subitem:
                        # Process the media list data
                        process_media_list_data(subitem, result)
            # Check if the item is a dictionary
            elif isinstance(item, dict):
                # Check if the item has the required structure
                if "string_map_data" in item:
                    # Process the string map data
                    process_string_map_data(item, result)

# Define the function to process the string list data
def process_string_list_data(data, result):
    # Check if the data has the required structure
    if "string_list_data" in data:
        # Iterate over the items in the string list
        for item in data["string_list_data"]:
            # Check if the item has the required structure
            if "href" in item and "timestamp" in item and "value" in item:
                # Add the item to the result dictionary
                result["User"].append(item["value"])
                result["Post Likes"].append(0)
                result["Story Likes"].append(0)
                result["Comments"].append(0)

# Define the function to process the media list data
def process_media_list_data(data, result):
    # Check if the data has the required structure
    if "media_list_data" in data:
        # Iterate over the items in the media list
        for item in data["media_list_data"]:
            # Check if the item has the required structure
            if "uri" in item:
                # Add the item to the result dictionary
                result["User"].append(item["uri"])
                result["Post Likes"].append(0)
                result["Story Likes"].append(0)
                result["Comments"].append(0)

# Define the function to process the string map data
def process_string_map_data(data, result):
    # Check if the data has the required structure
    if "string_map_data" in data:
        # Iterate over the items in the string map
        for item in data["string_map_data"]:
            # Check if the item has the required structure
            if "href" in item and "timestamp" in item and "value" in item:
                # Add the item to the result dictionary
                result["User"].append(item["value"])
                result["Post Likes"].append(0)
                result["Story Likes"].append(0)
                result["Comments"].append(0)

# Process the data
process_data()

# Sort the result dictionary by the number of interactions
result["User"] = sorted(result["User"], key=lambda x: (result["Post Likes"][result["User"].index(x)] + result["Story Likes"][result["User"].index(x)] + result["Comments"][result["User"].index(x)]), reverse=True)[:20]

# Write the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for user in result["User"]:
        writer.writerow([user, result["Post Likes"][result["User"].index(user)], result["Story Likes"][result["User"].index(user)], result["Comments"][result["User"].index(user)]])