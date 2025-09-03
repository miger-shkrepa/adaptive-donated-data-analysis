import os
import json
import csv

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    story_engagement = {}

    story_likes_path = os.path.join(root_dir, "story_interactions", "story_likes.json")
    if os.path.exists(story_likes_path):
        with open(story_likes_path, 'r', encoding='utf-8') as file:
            story_likes_data = json.load(file)
            for story_like in story_likes_data.get("story_activities_story_likes", []):
                title = story_like.get("title")
                if title:
                    story_engagement[title] = story_engagement.get(title, 0) + len(story_like.get("string_list_data", []))
    else:
        print("Warning: story_likes.json does not exist. Assuming no story engagement data.")

    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in story_engagement.items():
            writer.writerow({'User': user, 'Times Engaged': count})

except FileNotFoundError as e:
    print(e)
except json.JSONDecodeError as e:
    raise ValueError(f"Error: JSON decoding failed. {e}")
except Exception as e:
    raise Exception(f"Error: An unexpected error occurred. {e}")