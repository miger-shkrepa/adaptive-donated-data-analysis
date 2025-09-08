import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

engagement_data = {}

# Iterate over all files in the media/stories directory
for year_dir in os.listdir(os.path.join(root_dir, "media", "stories")):
    year_path = os.path.join(root_dir, "media", "stories", year_dir)
    if os.path.isdir(year_path):
        for file_name in os.listdir(year_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(year_path, file_name)
                try:
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for story in data.get("ig_stories", []):
                            owner = story.get("string_map_data", {}).get("Media Owner", {}).get("value")
                            if owner:
                                if owner not in engagement_data:
                                    engagement_data[owner] = 0
                                engagement_data[owner] += 1
                except FileNotFoundError:
                    print(f"FileNotFoundError: The file {file_path} does not exist.")

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, times_engaged in engagement_data.items():
        writer.writerow([user, times_engaged])