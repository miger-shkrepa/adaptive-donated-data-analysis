import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

engagements = {}

# Iterate over all the story folders
for year in os.listdir(os.path.join(root_dir, "media", "stories")):
    year_dir = os.path.join(root_dir, "media", "stories", year)
    if os.path.isdir(year_dir):
        for story in os.listdir(year_dir):
            if story.endswith(".json"):
                story_path = os.path.join(year_dir, story)
                try:
                    with open(story_path, "r") as f:
                        data = json.load(f)
                        for item in data["ig_stories"]:
                            if "cross_post_source" in item and "source_app" in item["cross_post_source"]:
                                user = item["cross_post_source"]["source_app"]
                                if user in engagements:
                                    engagements[user] += 1
                                else:
                                    engagements[user] = 1
                except FileNotFoundError:
                    print(f"FileNotFoundError: The file {story_path} does not exist.")

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Times Engaged"])
    for user, times in engagements.items():
        writer.writerow([user, times])