import os
import csv
import json
import datetime

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
        # Check if the current directory is 'ads_information'
        if dirpath.endswith('ads_information'):
            # Iterate over the files in the 'ads_and_topics' directory
            for filename in os.listdir(os.path.join(dirpath, 'ads_and_topics')):
                # Check if the file is 'ads_viewed.json'
                if filename == 'ads_viewed.json':
                    # Open the file and parse the JSON data
                    try:
                        with open(os.path.join(dirpath, 'ads_and_topics', filename), 'r') as json_file:
                            data = json.load(json_file)
                            # Check if the 'structure' key exists
                            if 'structure' in data:
                                # Iterate over the 'impressions_history_ads_seen' list
                                for item in data['structure']['impressions_history_ads_seen']:
                                    # Get the 'Time' value
                                    time_value = item['string_map_data']['Time']['value']
                                    # Parse the time value as a date
                                    try:
                                        date = datetime.datetime.strptime(time_value, '%Y-%m-%d')
                                    except ValueError:
                                        # If the time value is not a date, treat it as a week
                                        date = datetime.datetime.strptime(time_value, '%Y-%W')
                                    # Write the data to the CSV file
                                    writer.writerow([date.strftime('%Y-%m-%d'), 1, 'Daily'])
                                    writer.writerow([date.strftime('%Y-%W'), 1, 'Weekly'])
                    except FileNotFoundError:
                        # If the file does not exist, treat its contribution as 0
                        pass

        # Check if the current directory is 'connections'
        elif dirpath.endswith('connections'):
            # Iterate over the files in the 'followers_and_following' directory
            for filename in os.listdir(os.path.join(dirpath, 'followers_and_following')):
                # Check if the file is 'accounts_you've_favorited.json'
                if filename == 'accounts_you\'ve_favorited.json':
                    # Open the file and parse the JSON data
                    try:
                        with open(os.path.join(dirpath, 'followers_and_following', filename), 'r') as json_file:
                            data = json.load(json_file)
                            # Check if the 'structure' key exists
                            if 'structure' in data:
                                # Iterate over the 'relationships_feed_favorites' list
                                for item in data['structure']['relationships_feed_favorites']:
                                    # Get the 'Time' value
                                    time_value = item['string_list_data'][0]['timestamp']
                                    # Parse the time value as a date
                                    try:
                                        date = datetime.datetime.fromtimestamp(time_value)
                                    except ValueError:
                                        # If the time value is not a date, treat it as a week
                                        date = datetime.datetime.fromtimestamp(time_value)
                                    # Write the data to the CSV file
                                    writer.writerow([date.strftime('%Y-%m-%d'), 1, 'Daily'])
                                    writer.writerow([date.strftime('%Y-%W'), 1, 'Weekly'])
                    except FileNotFoundError:
                        # If the file does not exist, treat its contribution as 0
                        pass