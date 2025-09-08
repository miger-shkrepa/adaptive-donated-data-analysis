import csv
import json
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
        with open(os.path.join(root_dir, filename), "r") as f:
            # Load the JSON data
            data = json.load(f)
            # Check if the JSON data has a "structure" key
            if "structure" in data:
                # Iterate over the structure
                for key, value in data["structure"].items():
                    # Check if the value is a list
                    if isinstance(value, list):
                        # Iterate over the list
                        for item in value:
                            # Check if the item has a "title" key
                            if "title" in item:
                                # Add the title to the topics of interest list
                                topics_of_interest.append(item["title"])

# Write the topics of interest to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])
    writer.writerows([topic for topic in topics_of_interest if topic])

print("Query complete. Results saved to query_responses/results.csv")