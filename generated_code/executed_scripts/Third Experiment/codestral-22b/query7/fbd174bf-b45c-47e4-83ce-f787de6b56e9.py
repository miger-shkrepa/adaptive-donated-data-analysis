import os
import json
import csv

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the engagement count for each user
engagement_count = {}

# Traverse the directory structure
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if "story_activities_story_likes" in data:
                        for story in data["story_activities_story_likes"]:
                            if "string_map_data" in story:
                                for user, details in story["string_map_data"].items():
                                    if user not in engagement_count:
                                        engagement_count[user] = 0
                                    engagement_count[user] += 1
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

# Write the results to a CSV file
output_file = "query_responses/results.csv"
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Times Engaged"])
    for user, count in engagement_count.items():
        writer.writerow([user, count])