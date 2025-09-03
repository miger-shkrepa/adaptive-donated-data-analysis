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
            # Check if the JSON data contains the 'media' key
            if 'media' in data:
                # Load the JSON data as a Python object
                import json
                media_data = json.loads(data)
                # Check if the 'media' key contains a list of media objects
                if isinstance(media_data['media'], list):
                    # Iterate over the media objects
                    for media in media_data['media']:
                        # Check if the media object contains the 'interest_topics' key
                        if 'interest_topics' in media:
                            # Iterate over the interest topics
                            for topic in media['interest_topics']:
                                # Add the topic to the list of topics of interest
                                topics_of_interest.append(topic['topic_name'])

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Topics of Interest'])
    # Write the topics of interest
    for topic in topics_of_interest:
        writer.writerow([topic])