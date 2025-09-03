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

            # Check if the JSON data contains the required information
            if "story_activities_story_likes" in data["story_likes.json"]["structure"]:
                # Iterate over the story likes
                for story_like in data["story_likes.json"]["structure"]["story_activities_story_likes"]:
                    # Get the user ID and the timestamp
                    user_id = story_like["string_list_data"][0]["value"]
                    timestamp = story_like["string_list_data"][0]["timestamp"]

                    # Update the user engagement data
                    if user_id not in user_engagement:
                        user_engagement[user_id] = {}
                    if timestamp not in user_engagement[user_id]:
                        user_engagement[user_id][timestamp] = 0
                    user_engagement[user_id][timestamp] += 1

# Initialize the list to store the user engagement data
engagement_data = []

# Iterate over the user engagement data
for user_id, timestamps in user_engagement.items():
    # Get the maximum engagement time
    max_engagement_time = max(timestamps.values())

    # Add the user engagement data to the list
    engagement_data.append([user_id, max_engagement_time])

# Write the user engagement data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["User", "Times Engaged"])
    writer.writerows(engagement_data)