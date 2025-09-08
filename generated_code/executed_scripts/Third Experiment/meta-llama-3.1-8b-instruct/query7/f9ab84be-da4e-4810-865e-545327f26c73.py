import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the user engagement data
user_engagement = {}

# Iterate over each file in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required structure
            if 'story_activities_emoji_sliders' in data['structure']:
                # Iterate over each story activity
                for story_activity in data['structure']['story_activities_emoji_sliders']:
                    # Get the user name from the story activity
                    user_name = story_activity['title']

                    # Initialize the engagement count for the user
                    if user_name not in user_engagement:
                        user_engagement[user_name] = 0

                    # Increment the engagement count for the user
                    user_engagement[user_name] += 1

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create the CSV writer
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(['User', 'Times Engaged'])

    # Write the user engagement data to the CSV file
    for user, engagement in user_engagement.items():
        writer.writerow([user, engagement])