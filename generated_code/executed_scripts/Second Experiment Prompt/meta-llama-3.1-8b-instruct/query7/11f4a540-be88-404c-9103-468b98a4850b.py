import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize variables to store the results
user_engagement = {}

# Iterate over the 'your_instagram_activity' directory
for filename in os.listdir(os.path.join(root_dir, "your_instagram_activity")):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, "your_instagram_activity", filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            
            # Check if the JSON data contains the required information
            if "story_activities_story_likes" in data:
                # Iterate over the story likes
                for story in data["story_activities_story_likes"]:
                    # Get the user who posted the story
                    user = story["title"]
                    
                    # Increment the engagement count for the user
                    if user in user_engagement:
                        user_engagement[user] += 1
                    else:
                        user_engagement[user] = 1

# Create a CSV file to store the results
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)
    
    # Write the column headers
    writer.writerow(["User", "Times Engaged"])
    
    # Write the results
    for user, engagement in user_engagement.items():
        writer.writerow([user, engagement])