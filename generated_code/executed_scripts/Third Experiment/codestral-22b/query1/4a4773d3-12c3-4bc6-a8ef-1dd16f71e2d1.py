import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

topics_of_interest = []

# Check if reels.json exists
reels_file = os.path.join(root_dir, "media", "reels.json")
if os.path.exists(reels_file):
    with open(reels_file, 'r') as f:
        data = json.load(f)
        for reel in data["ig_reels_media"]:
            for media in reel["media"]:
                if "interest_topics" in media:
                    for topic in media["interest_topics"]:
                        topics_of_interest.append(topic["topic_name"])

# Check if stories.json exists
stories_file = os.path.join(root_dir, "media", "stories.json")
if os.path.exists(stories_file):
    with open(stories_file, 'r') as f:
        data = json.load(f)
        for story in data["ig_stories"]:
            if "interest_topics" in story:
                for topic in story["interest_topics"]:
                    topics_of_interest.append(topic["topic_name"])

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])