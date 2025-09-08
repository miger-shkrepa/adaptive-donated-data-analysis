import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def process_story_likes(data):
    story_engagement = {}
    if "story_activities_story_likes" in data:
        for entry in data["story_activities_story_likes"]:
            for item in entry["string_list_data"]:
                if "value" in item:
                    user = item["value"]
                    if user in story_engagement:
                        story_engagement[user] += 1
                    else:
                        story_engagement[user] = 1
    return story_engagement

def main():
    try:
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if not os.path.exists(story_likes_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User', 'Times Engaged'])
            return

        story_likes_data = load_json_file(story_likes_path)
        story_engagement = process_story_likes(story_likes_data)

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            for user, count in story_engagement.items():
                writer.writerow([user, count])

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()