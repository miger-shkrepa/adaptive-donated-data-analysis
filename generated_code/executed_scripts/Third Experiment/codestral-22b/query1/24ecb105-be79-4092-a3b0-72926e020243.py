import os
import csv
import json

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store topics of interest
topics_of_interest = []

# Define the path to the file containing topics of interest
file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "other_categories_used_to_reach_you.json")

# Check if the file exists
if os.path.exists(file_path):
    # Open the file and load the JSON data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Extract the topics of interest
    for item in data.get("label_values", []):
        topics_of_interest.append(item.get("label", ""))

# Define the output file path
output_file = "query_responses/results.csv"

# Write the topics of interest to a CSV file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Topics of Interest"])
    writer.writerows([[topic] for topic in topics_of_interest])