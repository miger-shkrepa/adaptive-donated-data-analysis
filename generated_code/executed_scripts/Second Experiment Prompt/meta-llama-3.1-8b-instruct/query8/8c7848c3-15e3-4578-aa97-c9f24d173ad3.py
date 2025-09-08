import csv
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
                process_json_data(data, result)

# Define the function to process the JSON data
def process_json_data(data, result):
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

# Define the function to process the item
def process_item(item, result):
    # Check if the item has a "string_map_data" key
    if "string_map_data" in item:
        # Get the "string_map_data" value
        string_map_data = item["string_map_data"]

        # Check if the "string_map_data" value is a dictionary
        if isinstance(string_map_data, dict):
            # Iterate over the items in the dictionary
            for key, value in string_map_data.items():
                # Check if the value is a dictionary with a "value" key
                if isinstance(value, dict) and "value" in value:
                    # Get the "value" value
                    value_value = value["value"]

                    # Check if the key is "Post Likes", "Story Likes", or "Comments"
                    if key in ["Post Likes", "Story Likes", "Comments"]:
                        # Add the value to the result dictionary
                        result["User"].append(item["title"])
                        result["Post Likes"].append(value_value)
                        result["Story Likes"].append(value_value)
                        result["Comments"].append(value_value)

# Process the data
process_data(root_dir)

# Save the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result["User"]))):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])

# Sort the result by the sum of Post Likes, Story Likes, and Comments
result["User"] = [x for _, x in sorted(zip([sum(map(int, y)) for y in zip(result["Post Likes"], result["Story Likes"], result["Comments"])], result["User"]))]

# Save the result to a CSV file
with open("query_responses/results.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
    for i in range(min(20, len(result["User"]))):
        writer.writerow([result["User"][i], result["Post Likes"][i], result["Story Likes"][i], result["Comments"][i]])