import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

engagements = {}

# Iterate over all the story interaction files
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file in ["story_likes.json", "countdowns.json"]:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for item in data.get("story_activities_story_likes", []) + data.get("story_activities_countdowns", []):
                        user = item["title"]
                        engagements[user] = engagements.get(user, 0) + len(item["string_list_data"])
            except FileNotFoundError:
                print(f"FileNotFoundError: The file {file_path} does not exist.")
            except json.JSONDecodeError:
                print(f"JSONDecodeError: The file {file_path} is not a valid JSON file.")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, times in engagements.items():
        writer.writerow([user, times])