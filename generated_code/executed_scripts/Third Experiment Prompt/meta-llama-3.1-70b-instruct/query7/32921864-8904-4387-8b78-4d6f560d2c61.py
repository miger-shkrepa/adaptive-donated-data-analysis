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

        # Iterate through story interactions files
        story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")
        if os.path.exists(story_interactions_dir):
            for file in os.listdir(story_interactions_dir):
                if file.endswith(".json"):
                    file_path = os.path.join(story_interactions_dir, file)
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        if "story_activities" in data:
                            for activity in data["story_activities"]:
                                if "title" in activity:
                                    user = activity["title"]
                                    if user not in story_engagement:
                                        story_engagement[user] = 0
                                    story_engagement[user] += 1

        # Write results to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
            for user, engagement in story_engagement.items():
                writer.writerow([user, engagement])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_story_engagement(root_dir)