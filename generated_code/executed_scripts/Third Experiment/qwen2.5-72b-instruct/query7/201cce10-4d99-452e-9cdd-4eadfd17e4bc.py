import os
import json
import csv

root_dir = "root_dir"

user_engagement = {}

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "story_likes.json":
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    story_activities = data.get("story_activities_story_likes", [])
                    for activity in story_activities:
                        string_list_data = activity.get("string_list_data", [])
                        for data_item in string_list_data:
                            title = activity.get("title")
                            if title:
                                user_engagement[title] = user_engagement.get(title, 0) + 1

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count in user_engagement.items():
            writer.writerow({'User': user, 'Times Engaged': count})

except FileNotFoundError as e:
    print(e)
except json.JSONDecodeError as e:
    raise ValueError(f"Error: JSON decoding failed. {e}")
except Exception as e:
    raise Exception(f"Error: An unexpected error occurred. {e}")