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
def process_data(root_dir):
    # Iterate over the files in the root directory
    for filename in os.listdir(root_dir):
        # Check if the file is a JSON file
        if filename.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(root_dir, filename), "r") as f:
                # Load the JSON data
                data = json.load(f)
                # Process the data
                process_json(data, result)

# Define the function to process a JSON object
def process_json(data, result):
    # Check if the data is a dictionary
    if isinstance(data, dict):
        # Iterate over the items in the dictionary
        for key, value in data.items():
            # Check if the value is a list
            if isinstance(value, list):
                # Iterate over the items in the list
                for item in value:
                    # Check if the item is a dictionary
                    if isinstance(item, dict):
                        # Process the item
                        process_item(item, result)
            # Check if the value is a dictionary
            elif isinstance(value, dict):
                # Process the value
                process_value(value, result)

# Define the function to process an item
def process_item(item, result):
    # Check if the item has a "title" key
    if "title" in item:
        # Get the title of the item
        title = item["title"]
        # Check if the title is a string
        if isinstance(title, str):
            # Add the title to the result dictionary
            result["User"].append(title)
            # Check if the item has a "string_list_data" key
            if "string_list_data" in item:
                # Get the string list data
                string_list_data = item["string_list_data"]
                # Check if the string list data is a list
                if isinstance(string_list_data, list):
                    # Iterate over the items in the list
                    for item in string_list_data:
                        # Check if the item is a dictionary
                        if isinstance(item, dict):
                            # Get the timestamp and value of the item
                            timestamp = item.get("timestamp", 0)
                            value = item.get("value", 0)
                            # Add the timestamp and value to the result dictionary
                            result["Post Likes"].append(timestamp)
                            result["Story Likes"].append(value)
                            # Check if the item has a "timestamp" key
                            if "timestamp" in item:
                                # Add the timestamp to the result dictionary
                                result["Comments"].append(timestamp)
            # Check if the item has a "media_list_data" key
            elif "media_list_data" in item:
                # Get the media list data
                media_list_data = item["media_list_data"]
                # Check if the media list data is a list
                if isinstance(media_list_data, list):
                    # Iterate over the items in the list
                    for item in media_list_data:
                        # Check if the item is a dictionary
                        if isinstance(item, dict):
                            # Get the timestamp and value of the item
                            timestamp = item.get("timestamp", 0)
                            value = item.get("value", 0)
                            # Add the timestamp and value to the result dictionary
                            result["Post Likes"].append(timestamp)
                            result["Story Likes"].append(value)
                            # Check if the item has a "timestamp" key
                            if "timestamp" in item:
                                # Add the timestamp to the result dictionary
                                result["Comments"].append(timestamp)

# Define the function to process a value
def process_value(value, result):
    # Check if the value is a dictionary
    if isinstance(value, dict):
        # Process the value
        process_item(value, result)

# Process the data
process_data(root_dir)

# Save the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result["User"]))):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])

# Print the result
print("Result:")
print("User\tPost Likes\tStory Likes\tComments")
for i in range(min(20, len(result["User"]))):
    print(f"{result['User'][i]}\t{result['Post Likes'][i]}\t{result['Story Likes'][i]}\t{result['Comments'][i]}")