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

def process_story_likes(data):
    story_likes = {}
    if "story_activities_story_likes" in data:
        for activity in data["story_activities_story_likes"]:
            for item in activity.get("string_list_data", []):
                if "value" in item:
                    username = item["value"]
                    if username in story_likes:
                        story_likes[username] += 1
                    else:
                        story_likes[username] = 1
    return story_likes

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if not os.path.exists(story_likes_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User', 'Times Engaged'])
            return

        story_likes_data = load_json_file(story_likes_path)
        story_likes = process_story_likes(story_likes_data)

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            for user, count in story_likes.items():
                writer.writerow([user, count])

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()