import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store topics of interest
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

# Write the results to a CSV file
with open(results_path, "w", newline="") as f:
    # Create a CSV writer object
    writer = csv.writer(f)

    # Write the column headers
    writer.writerow(["Topics of Interest"])

    # Write the topics of interest
    for topic in topics_of_interest:
        writer.writerow([topic])