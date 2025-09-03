import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Iterate over the JSON files in the 'personal_information' directory
for file in os.listdir(os.path.join(root_dir, "personal_information")):
    if file.endswith(".json"):
        # Open the JSON file and load its contents
        with open(os.path.join(root_dir, "personal_information", file), "r") as f:
            data = f.read()
            # Check if the JSON file contains the 'ig_reels_media' structure
            if "ig_reels_media" in data:
                # Iterate over the 'ig_reels_media' structure
                for media in eval(data)["structure"]["ig_reels_media"]:
                    # Iterate over the media items
                    for item in media["media"]:
                        # Check if the media item contains interest topics
                        if "interest_topics" in item:
                            # Extract the topics of interest
                            topics = [topic["topic_name"] for topic in item["interest_topics"]]
                            # Add the topics to the list
                            topics_of_interest.extend(topics)

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Topics of Interest"])
    # Write the topics of interest
    writer.writerow(topics_of_interest)