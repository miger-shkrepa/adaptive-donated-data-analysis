import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store topics of interest
topics_of_interest = []

# Traverse the directory structure
for foldername, subfolders, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "locations_of_interest.json":
            filepath = os.path.join(foldername, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
                for item in data["label_values"]:
                    topics_of_interest.append(item["label"])

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])