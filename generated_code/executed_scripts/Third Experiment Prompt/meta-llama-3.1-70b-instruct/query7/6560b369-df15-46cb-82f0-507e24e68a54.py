import os
import json
import csv

root_dir = "root_dir"

def get_story_engagement(root_dir):
    story_engagement = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Iterate through story likes files
        for file in os.listdir(os.path.join(root_dir, "your_instagram_activity", "likes")):
            if file.startswith("liked_posts") and file.endswith(".json"):
                file_path = os.path.join(root_dir, "your_instagram_activity", "likes", file)
                with open(file_path, "r") as f:
                    data = json.load(f)
                    for item in data.get("likes_media_likes", []):
                        for media in item.get("string_list_data", []):
                            if "value" in media and "owner" in media["value"]:
                                owner = media["value"]["owner"]
                                if owner not in story_engagement:
                                    story_engagement[owner] = 0
                                story_engagement[owner] += 1

        # Iterate through story interactions files
        for file in os.listdir(os.path.join(root_dir, "your_instagram_activity", "story_interactions")):
            if file.startswith("story_likes") and file.endswith(".json"):
                file_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", file)
                with open(file_path, "r") as f:
                    data = json.load(f)
                    for item in data.get("story_activities_story_likes", []):
                        for media in item.get("string_list_data", []):
                            if "value" in media and "owner" in media["value"]:
                                owner = media["value"]["owner"]
                                if owner not in story_engagement:
                                    story_engagement[owner] = 0
                                story_engagement[owner] += 1

        # Sort story engagement by value in descending order
        story_engagement = dict(sorted(story_engagement.items(), key=lambda item: item[1], reverse=True))

        # Write to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
            for user, times_engaged in story_engagement.items():
                writer.writerow([user, times_engaged])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_story_engagement(root_dir)