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

# Iterate over the 'ads_information' directory
for file in os.listdir(os.path.join(root_dir, "ads_information")):
    if file.endswith(".json"):
        # Open the JSON file and load its contents
        with open(os.path.join(root_dir, "ads_information", file), "r") as f:
            data = json.load(f)

        # Check if the file contains the 'topics_your_topics' structure
        if "topics_your_topics" in data["structure"]:
            # Extract the topics of interest from the JSON file
            topics_of_interest.extend([topic["value"] for topic in data["structure"]["topics_your_topics"]])

# Write the topics of interest to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    writer.writerows([[topic] for topic in topics_of_interest])

print("Query completed successfully.")