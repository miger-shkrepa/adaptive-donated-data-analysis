import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the user and times engaged
users = []
times_engaged = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if 'story_interactions' in data and 'story_likes.json' in data['story_interactions']:
                # Open the story likes JSON file
                with open(os.path.join(root_dir, 'story_interactions', 'story_likes.json'), 'r') as story_likes_file:
                    # Load the story likes JSON data
                    story_likes_data = eval(story_likes_file.read())

                    # Iterate over the story likes data
                    for story_like in story_likes_data['structure']['story_activities_story_likes']:
                        # Check if the story like contains the required information
                        if 'string_list_data' in story_like and len(story_like['string_list_data']) > 0:
                            # Extract the user and times engaged from the story like
                            user = story_like['title']
                            times_engaged.append(story_like['string_list_data'][0]['timestamp'])

                            # Add the user to the list if it's not already there
                            if user not in users:
                                users.append(user)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csv_file:
    # Create the CSV writer
    writer = csv.writer(csv_file)

    # Write the column headers
    writer.writerow(['User', 'Times Engaged'])

    # Write the data to the CSV file
    for user, times_engaged_value in zip(users, times_engaged):
        writer.writerow([user, times_engaged_value])