import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

def process_story_interactions(data):
    story_engagements = {}
    if "story_activities_story_likes" in data:
        for activity in data["story_activities_story_likes"]:
            for entry in activity.get("string_list_data", []):
                if "value" in entry:
                    user = entry["value"]
                    story_engagements[user] = story_engagements.get(user, 0) + 1
    return story_engagements

def process_stories(data):
    story_engagements = {}
    if "ig_stories" in data:
        for story in data["ig_stories"]:
            if "media_metadata" in story and "photo_metadata" in story["media_metadata"]:
                for exif in story["media_metadata"]["photo_metadata"]["exif_data"]:
                    if "device_id" in exif:
                        user = exif["device_id"]
                        story_engagements[user] = story_engagements.get(user, 0) + 1
    return story_engagements

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        story_interactions_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        stories_path = os.path.join(root_dir, "your_instagram_activity", "content", "stories.json")

        story_interactions_data = {}
        stories_data = {}

        if os.path.exists(story_interactions_path):
            story_interactions_data = load_json_file(story_interactions_path)
        if os.path.exists(stories_path):
            stories_data = load_json_file(stories_path)

        story_engagements = process_story_interactions(story_interactions_data)
        story_engagements.update(process_stories(stories_data))

        if not story_engagements:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["User", "Times Engaged"])
            return

        sorted_engagements = sorted(story_engagements.items(), key=lambda x: x[1], reverse=True)

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
            for user, count in sorted_engagements:
                writer.writerow([user, count])

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()