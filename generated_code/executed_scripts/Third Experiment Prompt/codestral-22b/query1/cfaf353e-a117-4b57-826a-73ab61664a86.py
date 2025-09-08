import os
import json
import csv

root_dir = "root_dir"
output_file = "query_responses/results.csv"

# Create the output directory if it doesn't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Walk through the directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "reels.json":
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    for reel in data.get("ig_reels_media", []):
                        for media in reel.get("media", []):
                            for topic in media.get("interest_topics", []):
                                topics_of_interest.append(topic.get("topic_name"))
            except FileNotFoundError:
                raise FileNotFoundError(f"FileNotFoundError: The file {filepath} does not exist.")
            except json.JSONDecodeError:
                raise ValueError(f"ValueError: The file {filepath} is not a valid JSON file.")

# Write the topics of interest to a CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])