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
        # Open the JSON file and load its contents
        with open(os.path.join(root_dir, filename), "r") as f:
            data = json.load(f)

        # Check if the JSON file contains the "your_topics" key
        if "your_topics" in data:
            # Iterate over the values in the "your_topics" key
            for value in data["your_topics"].values():
                # Check if the value is a dictionary
                if isinstance(value, dict):
                    # Check if the dictionary contains the "topics" key
                    if "topics" in value:
                        # Iterate over the values in the "topics" key
                        for topic in value["topics"]:
                            # Add the topic to the list of topics of interest
                            topics_of_interest.append(topic)

# Write the topics of interest to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])
    writer.writerows([topic for topic in topics_of_interest if topic])

print("Query complete. Results saved to query_responses/results.csv")