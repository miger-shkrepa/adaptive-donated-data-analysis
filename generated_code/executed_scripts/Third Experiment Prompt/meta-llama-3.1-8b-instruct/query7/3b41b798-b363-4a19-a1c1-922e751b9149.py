import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement counts for each user
engagement_counts = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Parse the JSON data
            import json
            parsed_data = json.loads(data)
            
            # Check if the JSON data contains the required information
            if 'story_activities_story_likes' in parsed_data['story_interactions']:
                # Iterate over the story likes
                for story_like in parsed_data['story_interactions']['story_activities_story_likes']:
                    # Get the user who posted the story
                    user = story_like['title']
                    # Get the timestamp of the story like
                    timestamp = story_like['string_list_data'][0]['timestamp']
                    # Increment the engagement count for the user
                    if user in engagement_counts:
                        engagement_counts[user].append(timestamp)
                    else:
                        engagement_counts[user] = [timestamp]

# Initialize a list to store the CSV rows
csv_rows = []

# Iterate over the engagement counts
for user, timestamps in engagement_counts.items():
    # Calculate the total number of times the user was engaged with
    total_engagements = len(timestamps)
    # Append the CSV row
    csv_rows.append([user, total_engagements])

# Write the CSV rows to the output file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['User', 'Times Engaged'])
    # Write the CSV rows
    writer.writerows(csv_rows)