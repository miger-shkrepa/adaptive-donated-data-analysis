import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Define the path to the topics of interest file
topics_file_path = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")

# Check if the topics file exists
if os.path.exists(topics_file_path):
    # Open the topics file
    with open(topics_file_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the topics of interest
        for topic in data["topics_your_topics"]:
            topics_of_interest.append(topic["string_map_data"]["Name"]["value"])

# Define the path to the output file
output_file_path = "query_responses/results.csv"

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Write the topics of interest to a CSV file
with open(output_file_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])