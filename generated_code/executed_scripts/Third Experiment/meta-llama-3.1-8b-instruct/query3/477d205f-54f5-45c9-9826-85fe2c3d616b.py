import csv
import os
import json

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
dates = []
posts_viewed_daily = []
posts_viewed_weekly = []

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
                for ad, topic in data['ads_information']['ads_and_topics'].items():
                    # Check if the ad is a posts viewed ad
                    if ad == 'posts_viewed.json':
                        # Iterate over the impressions history posts seen
                        for post in topic['structure']['impressions_history_posts_seen']:
                            # Get the timestamp
                            timestamp = post['string_map_data']['Time']['timestamp']
                            # Check if the timestamp is a daily timestamp
                            if timestamp % 7 == 0:
                                # Add the date to the list of dates
                                dates.append('2025-01-18')
                                # Increment the daily posts viewed count
                                posts_viewed_daily.append(1)
                            # Check if the timestamp is a weekly timestamp
                            elif timestamp % 7 == 6:
                                # Add the week to the list of dates
                                dates.append('Week 2025-02')
                                # Increment the weekly posts viewed count
                                posts_viewed_weekly.append(1)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    # Create the CSV writer
    writer = csv.writer(file)
    # Write the column headers
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    # Write the data
    for i in range(len(dates)):
        # Write the date
        writer.writerow([dates[i], posts_viewed_daily[i] if i < len(posts_viewed_daily) else 0, 'Daily'])
        # Write the week
        writer.writerow([dates[i], posts_viewed_weekly[i] if i < len(posts_viewed_weekly) else 0, 'Weekly'])