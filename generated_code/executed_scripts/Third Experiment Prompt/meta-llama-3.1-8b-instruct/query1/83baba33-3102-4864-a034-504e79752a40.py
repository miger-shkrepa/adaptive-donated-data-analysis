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
                # Iterate over the items in the "structure" key
                for item in data["structure"]:
                    # Check if the item has a "topics_your_topics" key
                    if "topics_your_topics" in item:
                        # Iterate over the topics in the "topics_your_topics" key
                        for topic in item["topics_your_topics"]:
                            # Add the topic to the list of topics of interest
                            topics_of_interest.append(topic["title"])

# Write the topics of interest to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])
    writer.writerows([topic for topic in topics_of_interest])

print("Query complete. Results saved to query_responses/results.csv")