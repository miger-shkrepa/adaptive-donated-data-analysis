import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_weekly_messages(root_dir):
    weekly_messages = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate through subfolders in 'your_instagram_activity'
        activity_dir = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(activity_dir):
            return weekly_messages

        for subfolder in os.listdir(activity_dir):
            if subfolder == "likes":
                likes_dir = os.path.join(activity_dir, subfolder)
                likes_file = os.path.join(likes_dir, "liked_posts.json")
                if not os.path.exists(likes_file):
                    continue

                with open(likes_file, "r") as f:
                    likes_data = json.load(f)
                    for like in likes_data["likes_media_likes"]:
                        timestamp = like["string_list_data"][0]["timestamp"]
                        week = datetime.fromtimestamp(timestamp).strftime("%Y-%W")
                        if week not in weekly_messages:
                            weekly_messages[week] = 0
                        weekly_messages[week] += 1

        return weekly_messages

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_to_csv(weekly_messages):
    with open("query_responses/results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Week", "Messages Sent"])
        for week, messages in weekly_messages.items():
            writer.writerow([f"Week {week}", messages])

weekly_messages = get_weekly_messages(root_dir)
save_to_csv(weekly_messages)