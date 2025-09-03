import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def process_stories_data(stories_data):
    story_engagement = {}
    for story in stories_data.get("ig_stories", []):
        media_owner = story.get("media_owner")
        if media_owner:
            story_engagement[media_owner] = story_engagement.get(media_owner, 0) + 1
    return story_engagement

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        stories_file_path = os.path.join(root_dir, "your_instagram_activity", "content", "stories.json")
        if not os.path.exists(stories_file_path):
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User', 'Times Engaged'])
            return

        stories_data = load_json_file(stories_file_path)
        story_engagement = process_stories_data(stories_data)

        if not story_engagement:
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['User', 'Times Engaged'])
            return

        sorted_engagement = sorted(story_engagement.items(), key=lambda x: x[1], reverse=True)
        top_engagement = sorted_engagement[0]

        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            writer.writerow(top_engagement)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()