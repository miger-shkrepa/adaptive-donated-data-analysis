import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")

if not os.path.exists(story_likes_path):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
else:
    with open(story_likes_path, 'r') as f:
        data = json.load(f)

    story_likes = data["story_activities_story_likes"]

    user_engagement = {}
    for story in story_likes:
        user = story["title"]
        if user in user_engagement:
            user_engagement[user] += 1
        else:
            user_engagement[user] = 1

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, times_engaged in user_engagement.items():
            writer.writerow([user, times_engaged])