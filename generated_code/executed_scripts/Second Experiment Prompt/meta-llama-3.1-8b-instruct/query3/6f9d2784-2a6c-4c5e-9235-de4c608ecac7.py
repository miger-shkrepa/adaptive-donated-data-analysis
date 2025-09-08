import csv
import os
import datetime
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as json_file:
                        data = json.load(json_file)
                        if 'ads_information' in data and 'ads_and_topics' in data['ads_information'] and 'ads_viewed.json' in data['ads_and_topics']:
                            # Extract the impressions history ads seen data
                            impressions_history_ads_seen = data['ads_information']['ads_and_topics']['ads_viewed.json']['structure']['impressions_history_ads_seen']
                            # Extract the impressions history posts seen data
                            impressions_history_posts_seen = data['ads_information']['ads_and_topics']['posts_viewed.json']['structure']['impressions_history_posts_seen']
                            # Calculate the total posts viewed
                            total_posts_viewed = len(impressions_history_ads_seen) + len(impressions_history_posts_seen)
                            # Calculate the date/week
                            date = datetime.datetime.now().strftime('%Y-%m-%d')
                            week = datetime.datetime.now().strftime('%Y-%W')
                            # Write the data to the CSV file
                            writer.writerow([date, total_posts_viewed, 'Daily'])
                            writer.writerow([week, total_posts_viewed, 'Weekly'])
                except FileNotFoundError:
                    # If the file does not exist, treat its contribution as 0
                    continue
                except ValueError as e:
                    # If there is a value error, print the error message
                    print(f"Error: {e}")