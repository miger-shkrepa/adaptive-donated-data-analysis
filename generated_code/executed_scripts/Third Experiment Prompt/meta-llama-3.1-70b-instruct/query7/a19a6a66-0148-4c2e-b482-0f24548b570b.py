import os
import json
import csv

root_dir = "root_dir"

def get_story_engagements(root_dir):
    story_engagements = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Iterate through connections directory
        connections_dir = os.path.join(root_dir, "connections", "followers_and_following")
        if os.path.exists(connections_dir):
            for file in os.listdir(connections_dir):
                if file.endswith(".json"):
                    file_path = os.path.join(connections_dir, file)
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        if "relationships_following" in data:
                            for item in data["relationships_following"]:
                                user = item["title"]
                                if user not in story_engagements:
                                    story_engagements[user] = 0
                                story_engagements[user] += len(item["string_list_data"])

        # Iterate through your_instagram_activity directory
        activity_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")
        if os.path.exists(activity_dir):
            for file in os.listdir(activity_dir):
                if file.endswith(".json"):
                    file_path = os.path.join(activity_dir, file)
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        if "story_activities_story_likes" in data:
                            for item in data["story_activities_story_likes"]:
                                user = item["title"]
                                if user not in story_engagements:
                                    story_engagements[user] = 0
                                story_engagements[user] += len(item["string_list_data"])

        # Sort story engagements by value in descending order
        sorted_engagements = sorted(story_engagements.items(), key=lambda x: x[1], reverse=True)

        # Write to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
            for user, engagement in sorted_engagements:
                writer.writerow([user, engagement])

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise ValueError("Error: " + str(e))

get_story_engagements(root_dir)