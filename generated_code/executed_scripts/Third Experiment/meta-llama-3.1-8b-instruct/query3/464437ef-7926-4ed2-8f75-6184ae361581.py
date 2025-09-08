import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
date_week_list = []
posts_viewed_list = []
type_list = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON file contains the required data
            if 'story_interactions' in data:
                # Iterate over the story interactions
                for interaction in data['story_interactions'].values():
                    # Check if the interaction is a JSON file
                    if interaction['type'] == 'json':
                        # Check if the interaction contains the required data
                        if 'story_activities_emoji_sliders' in interaction['structure']:
                            # Iterate over the story activities
                            for activity in interaction['structure']['story_activities_emoji_sliders']:
                                # Check if the activity contains the required data
                                if 'string_list_data' in activity:
                                    # Iterate over the string list data
                                    for item in activity['string_list_data']:
                                        # Check if the item contains the required data
                                        if 'timestamp' in item and 'value' in item:
                                            # Get the date or week from the timestamp
                                            if item['timestamp'] < 86400:
                                                date_week = datetime.datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d')
                                            else:
                                                date_week = datetime.datetime.fromtimestamp(item['timestamp']).strftime('Week %Y-W%W')

                                            # Get the posts viewed and type
                                            posts_viewed = 1
                                            type = 'Daily' if item['timestamp'] < 86400 else 'Weekly'

                                            # Append the data to the lists
                                            date_week_list.append(date_week)
                                            posts_viewed_list.append(posts_viewed)
                                            type_list.append(type)

# Check if the lists are empty
if not date_week_list:
    # Write the column headers to the CSV file
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
else:
    # Write the data to the CSV file
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
        writer.writerows(zip(date_week_list, posts_viewed_list, type_list))