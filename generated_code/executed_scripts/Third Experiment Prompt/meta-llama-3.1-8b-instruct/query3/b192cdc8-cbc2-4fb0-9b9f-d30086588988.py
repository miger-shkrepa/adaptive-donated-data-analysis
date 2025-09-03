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
            if filename == 'posts_viewed.json':
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as file:
                        data = json.load(file)
                        if 'structure' in data and 'impressions_history_posts_seen' in data['structure']:
                            for item in data['structure']['impressions_history_posts_seen']:
                                for post in item['string_map_data'].values():
                                    if 'timestamp' in post and 'value' in post:
                                        date = datetime.datetime.fromtimestamp(post['timestamp'])
                                        if date.weekday() == 0:  # Monday
                                            week = date.strftime('%Y-%W')
                                        else:
                                            week = date.strftime('%Y-%m-%d')
                                        writer.writerow([week, 1, 'Weekly'])
                                    elif 'value' in post:
                                        date = datetime.datetime.fromtimestamp(0)  # default date
                                        writer.writerow([date.strftime('%Y-%m-%d'), 1, 'Daily'])
                except FileNotFoundError:
                    print(f"Error: File {filepath} not found.")
                except json.JSONDecodeError:
                    print(f"Error: Failed to parse JSON in file {filepath}.")
                except KeyError:
                    print(f"Error: Missing key in file {filepath}.")