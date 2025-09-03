import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Define the path to the locations_of_interest.json file
locations_of_interest_path = os.path.join(root_dir, "information_about_you", "locations_of_interest.json")

# Check if the locations_of_interest.json file exists
if os.path.exists(locations_of_interest_path):
    # Open the locations_of_interest.json file
    with open(locations_of_interest_path, "r") as f:
        # Load the JSON data
        data = json.load(f)

        # Extract the topics of interest
        for item in data["label_values"]:
            if "label" in item:
                topics_of_interest.append(item["label"])

# Define the path to the results.csv file
results_path = "query_responses/results.csv"

# Create the directory if it does not exist
os.makedirs(os.path.dirname(results_path), exist_ok=True)

# Write the results to a CSV file
with open(results_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])