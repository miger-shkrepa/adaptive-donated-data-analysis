import os
import csv
from collections import defaultdict

root_dir = "root_dir"

def get_story_likes_data(file_path):
    try:
        with open(file_path, 'r') as file:
            import json
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The story_likes.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The story_likes.json file is not a valid JSON file.")

def aggregate_story_likes(data):
    engagement_count = defaultdict(int)
    for activity in data.get('story_activities_story_likes', []):
        for item in activity.get('string_list_data', []):
            user = item.get('value')
            if user:
                engagement_count[user] += 1
    return engagement_count

def write_csv(engagement_count, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            for user, count in engagement_count.items():
                writer.writerow([user, count])
    except IOError:
        raise IOError("IOError: Failed to write to the CSV file.")

def main():
    story_likes_path = os.path.join(root_dir, 'story_interactions', 'story_likes.json')
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    if not os.path.exists(story_likes_path):
        write_csv({}, 'query_responses/results.csv')
        return

    data = get_story_likes_data(story_likes_path)
    engagement_count = aggregate_story_likes(data)
    write_csv(engagement_count, 'query_responses/results.csv')

if __name__ == "__main__":
    main()