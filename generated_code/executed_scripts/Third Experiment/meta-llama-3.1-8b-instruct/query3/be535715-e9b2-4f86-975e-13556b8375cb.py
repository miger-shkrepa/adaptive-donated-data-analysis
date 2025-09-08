import csv
import os
import json
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the result list
result = []

# Iterate over each file in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)

            # Check if the JSON data has a 'story_activities_story_likes' key
            if 'story_activities_story_likes' in data['structure']:
                # Iterate over each story activity
                for story_activity in data['structure']['story_activities_story_likes']:
                    # Check if the story activity has a 'string_list_data' key
                    if 'string_list_data' in story_activity:
                        # Iterate over each string list data
                        for string_list_data in story_activity['string_list_data']:
                            # Check if the string list data has a 'timestamp' key
                            if 'timestamp' in string_list_data:
                                # Get the timestamp
                                timestamp = string_list_data['timestamp']

                                # Check if the timestamp is a week
                                if timestamp % 7 == 0:
                                    # Get the week number
                                    week_number = timestamp // 7

                                    # Append the result to the result list
                                    result.append([f"Week {week_number}", 1, 'Weekly'])
                                else:
                                    # Append the result to the result list
                                    result.append([datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'), 1, 'Daily'])

# Write the result to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    writer.writerows(result)

print("Query completed successfully.")