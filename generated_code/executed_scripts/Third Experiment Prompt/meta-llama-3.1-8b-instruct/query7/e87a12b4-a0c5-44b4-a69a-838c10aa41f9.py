import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the user engagement dictionary
user_engagement = {}

# Iterate over the directory structure
for dir, _, files in os.walk(root_dir):
    # Check if the directory is 'your_instagram_activity/media'
    if dir.endswith('your_instagram_activity/media'):
        # Iterate over the files in the directory
        for file in files:
            # Check if the file is 'stories.json'
            if file == 'stories.json':
                # Open the file and load the JSON data
                with open(os.path.join(dir, file), 'r') as f:
                    data = json.load(f)
                # Iterate over the stories in the file
                for story in data['ig_stories']:
                    # Get the user who posted the story
                    user = story['cross_post_source']['source_app']
                    # Get the timestamp of the story
                    timestamp = story['creation_timestamp']
                    # Increment the user's engagement count
                    user_engagement[user] = user_engagement.get(user, 0) + 1

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['User', 'Times Engaged'])
    # Write the user engagement data
    for user, engagement in user_engagement.items():
        writer.writerow([user, engagement])