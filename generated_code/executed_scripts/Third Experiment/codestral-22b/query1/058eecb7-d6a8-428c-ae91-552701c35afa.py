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

# Define the path to the JSON file containing the topics of interest
json_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "accounts_you're_not_interested_in.json")

# Check if the JSON file exists
if os.path.exists(json_file_path):
    # Open the JSON file
    with open(json_file_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the topics of interest
        for item in data["impressions_history_recs_hidden_authors"]:
            if "string_map_data" in item and "Benutzername" in item["string_map_data"]:
                topics_of_interest.append(item["string_map_data"]["Benutzername"]["value"])
else:
    print("Warning: The JSON file containing the topics of interest does not exist.")

# Define the path to the output CSV file
output_file_path = "query_responses/results.csv"

# Write the topics of interest to a CSV file
with open(output_file_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])