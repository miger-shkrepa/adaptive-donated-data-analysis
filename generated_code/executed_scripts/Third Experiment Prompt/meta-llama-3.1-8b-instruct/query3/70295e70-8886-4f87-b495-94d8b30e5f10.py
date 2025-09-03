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

    # Iterate over the daily posts
    daily_posts = 0
    for date in os.listdir(os.path.join(root_dir, 'ads_information', 'ads_and_topics')):
        if date.endswith('.json'):
            try:
                with open(os.path.join(root_dir, 'ads_information', 'ads_and_topics', date), 'r') as f:
                    data = json.load(f)
                    if 'structure' in data:
                        if 'ads_viewed.json' in date:
                            for item in data['structure']['impressions_history_ads_seen']:
                                if 'string_map_data' in item:
                                    for key, value in item['string_map_data'].items():
                                        if key == 'Time':
                                            timestamp = value['timestamp']
                                            date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                                            writer.writerow([date_str, 1, 'Daily'])
                                            daily_posts += 1
                                        elif key == 'Author':
                                            writer.writerow([date_str, 1, 'Daily'])
                                            daily_posts += 1
                        elif 'posts_viewed.json' in date:
                            for item in data['structure']['impressions_history_posts_seen']:
                                if 'string_map_data' in item:
                                    for key, value in item['string_map_data'].items():
                                        if key == 'Time':
                                            timestamp = value['timestamp']
                                            week_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%W')
                                            writer.writerow([week_str, 1, 'Weekly'])
                                            weekly_posts += 1
            except FileNotFoundError:
                print(f"Error: The file {date} does not exist.")

# Close the CSV writer
csvfile.close()