import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
date_week = []
posts_viewed = []
type = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            # Check if the JSON data contains the required information
            if 'ads_information' in data and 'ads_and_topics' in data['ads_information']:
                # Iterate over the ads and topics
                for topic in data['ads_information']['ads_and_topics'].values():
                    # Check if the topic is a JSON file
                    if topic['type'] == 'json':
                        # Check if the topic contains the required information
                        if 'structure' in topic and 'impressions_history_posts_seen' in topic['structure']:
                            # Iterate over the impressions history posts seen
                            for post in topic['structure']['impressions_history_posts_seen']:
                                # Check if the post contains the required information
                                if 'string_map_data' in post and 'Time' in post['string_map_data']:
                                    # Extract the date and week from the timestamp
                                    timestamp = post['string_map_data']['Time']['timestamp']
                                    if timestamp % 7 == 0:
                                        date_week.append(f"Week {timestamp // 7}-{timestamp // 7 + 1}")
                                        posts_viewed.append(1)
                                        type.append('Weekly')
                                    else:
                                        date_week.append(f"{timestamp // 1000000}-{timestamp // 1000 % 10000:02d}-{timestamp % 1000}")
                                        posts_viewed.append(1)
                                        type.append('Daily')

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    writer.writerows(zip(date_week, posts_viewed, type))