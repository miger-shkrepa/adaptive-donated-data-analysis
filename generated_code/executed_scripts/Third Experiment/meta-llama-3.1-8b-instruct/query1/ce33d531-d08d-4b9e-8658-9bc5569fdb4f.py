import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Parse the JSON data
            import json
            parsed_data = json.loads(data)
            # Check if the JSON data contains the required structure
            if 'monetization' in parsed_data and 'eligibility.json' in parsed_data['monetization']:
                # Extract the topics of interest from the JSON data
                topics_of_interest.extend([item['title'] for item in parsed_data['monetization']['eligibility.json']['structure']['monetization_eligibility']])

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])
    writer.writerow(topics_of_interest)