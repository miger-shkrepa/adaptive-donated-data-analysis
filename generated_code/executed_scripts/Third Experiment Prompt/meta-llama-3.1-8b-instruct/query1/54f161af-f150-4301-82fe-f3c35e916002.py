import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Iterate over the subdirectories in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Check if the subdirectory is 'ads_information'
    if dirpath.endswith('ads_information'):
        # Iterate over the files in the subdirectory
        for filename in filenames:
            # Check if the file is 'recommended_topics.json'
            if filename == 'recommended_topics.json':
                # Open the file and read its contents
                with open(os.path.join(dirpath, filename), 'r') as f:
                    data = f.read()
                    # Parse the JSON data
                    import json
                    data = json.loads(data)
                    # Extract the topics of interest
                    topics_of_interest.extend([item['Name'] for item in data['topics_your_topics']])

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Topics of Interest'])
    writer.writerows([[topic] for topic in topics_of_interest])