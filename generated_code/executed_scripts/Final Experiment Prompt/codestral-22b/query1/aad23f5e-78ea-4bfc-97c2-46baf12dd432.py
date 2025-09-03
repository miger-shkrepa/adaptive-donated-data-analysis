import json
import csv
import os

# Declare the root directory
root_dir = "root_dir"

# Define the path to the JSON file
json_file_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Check if the JSON file exists
if os.path.exists(json_file_path):
    try:
        # Open the JSON file
        with open(json_file_path, 'r') as file:
            # Load the JSON data
            data = json.load(file)

        # Extract the topics of interest
        for topic in data.get("topics_your_topics", []):
            name = topic.get("string_map_data", {}).get("Name", {}).get("value", "")
            if name:
                topics_of_interest.append(name)
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not correctly formatted.")
else:
    raise FileNotFoundError("Error: The JSON file does not exist.")

# Define the path to the CSV file
csv_file_path = "query_responses/results.csv"

# Write the topics of interest to a CSV file
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Topics of Interest"])
    writer.writerows([[topic] for topic in topics_of_interest])