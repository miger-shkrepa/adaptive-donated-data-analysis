import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the dictionary to store the user engagement data
user_engagement = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the 'media' key
            if 'media' in data:
                # Iterate over the media items
                for media in data['media']:
                    # Check if the media item contains the 'stories.json' key
                    if 'stories.json' in media:
                        # Open the 'stories.json' file
                        with open(os.path.join(root_dir, media['stories.json']), 'r') as stories_file:
                            # Load the 'stories.json' data
                            stories_data = eval(stories_file.read())

                            # Iterate over the stories
                            for story in stories_data['ig_stories']:
                                # Check if the story contains the 'sender_name' key
                                if 'sender_name' in story:
                                    # Get the sender name
                                    sender_name = story['sender_name']

                                    # Check if the sender name is already in the user engagement dictionary
                                    if sender_name in user_engagement:
                                        # Increment the engagement count for the sender
                                        user_engagement[sender_name] += 1
                                    else:
                                        # Add the sender to the user engagement dictionary with an engagement count of 1
                                        user_engagement[sender_name] = 1

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create the CSV writer
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(['User', 'Times Engaged'])

    # Iterate over the user engagement dictionary
    for user, engagement in user_engagement.items():
        # Write the user engagement data to the CSV file
        writer.writerow([user, engagement])