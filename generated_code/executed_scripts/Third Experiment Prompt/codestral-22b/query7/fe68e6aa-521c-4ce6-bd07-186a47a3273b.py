import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

engagements = {}

# Iterate over all the directories and files in the root directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "story_likes.json":
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    for engagement in data["story_activities_story_likes"]:
                        user = engagement["title"]
                        times_engaged = len(engagement["string_list_data"])
                        if user in engagements:
                            engagements[user] += times_engaged
                        else:
                            engagements[user] = times_engaged
            except FileNotFoundError:
                print(f"FileNotFoundError: The file {filepath} does not exist.")
            except json.JSONDecodeError:
                print(f"JSONDecodeError: The file {filepath} is not a valid JSON file.")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, times_engaged in engagements.items():
        writer.writerow([user, times_engaged])