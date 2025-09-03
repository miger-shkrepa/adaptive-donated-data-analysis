import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = []

# Iterate over the directory structure
for dir, _, files in os.walk(root_dir):
    # Check if the current directory is 'your_instagram_activity'
    if dir.endswith('your_instagram_activity'):
        # Iterate over the files in the current directory
        for file in files:
            # Check if the file is 'story_interactions'
            if file == 'story_interactions.json':
                # Open the file and read its contents
                with open(os.path.join(dir, file), 'r') as f:
                    data = json.load(f)
                # Iterate over the story interactions
                for story in data['story_activities_story_likes']:
                    # Extract the user and times engaged
                    user = story['title']
                    times_engaged = len(story['string_list_data'])
                    # Append the result to the results list
                    results.append((user, times_engaged))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Times Engaged'])
    writer.writerows(results)