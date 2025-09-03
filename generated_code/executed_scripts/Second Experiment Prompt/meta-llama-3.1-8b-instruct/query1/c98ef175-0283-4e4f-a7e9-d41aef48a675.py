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
            # Check if the JSON data has a "topics_your_topics" key
            if "topics_your_topics" in data:
                # Iterate over the topics of interest
                for topic in data["topics_your_topics"]:
                    # Extract the topic name
                    topic_name = topic["string_map_data"]["Name"]["value"]
                    # Add the topic name to the list
                    topics_of_interest.append(topic_name)

# Create a CSV file to store the results
with open("query_responses/results.csv", "w", newline="") as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Topics of Interest"])
    # Write the topics of interest
    writer.writerows([topic] for topic in topics_of_interest)

print("Query complete. Results saved to query_responses/results.csv")