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
        with open(os.path.join(root_dir, filename), "r") as file:
            # Load the JSON data
            data = json.load(file)
            # Check if the JSON data has a "structure" key
            if "structure" in data:
                # Iterate over the keys in the "structure" dictionary
                for key, value in data["structure"].items():
                    # Check if the key is "topics_your_topics"
                    if key == "topics_your_topics":
                        # Iterate over the items in the "topics_your_topics" list
                        for item in value:
                            # Extract the topic of interest
                            topic = item["string_map_data"]["Name"]["value"]
                            # Add the topic to the list
                            topics_of_interest.append(topic)

# Write the topics of interest to a CSV file
with open("query_responses/results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Topics of Interest"])
    writer.writerows([topic] for topic in topics_of_interest)