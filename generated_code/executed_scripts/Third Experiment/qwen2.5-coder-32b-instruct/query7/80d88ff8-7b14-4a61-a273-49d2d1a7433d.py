import os
import csv
import json

root_dir = "root_dir"

def get_story_likes(root_directory):
    story_likes_path = os.path.join(root_directory, "story_interactions", "story_likes.json")
    
    if not os.path.exists(root_directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(story_likes_path):
        return {}

    try:
        with open(story_likes_path, 'r', encoding='utf-8') as file:
            story_likes_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The story_likes.json file is not properly formatted.")
    
    story_likes = story_likes_data.get("story_activities_story_likes", [])
    engagement_count = {}

    for story_like in story_likes:
        title = story_like.get("title", "")
        if title:
            engagement_count[title] = engagement_count.get(title, 0) + 1

    return engagement_count

def write_csv(engagement_data, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
            for user, count in engagement_data.items():
                writer.writerow([user, count])
    except IOError:
        raise IOError("IOError: Failed to write to the CSV file.")

def main():
    try:
        engagement_data = get_story_likes(root_dir)
        write_csv(engagement_data, 'query_responses/results.csv')
    except (FileNotFoundError, ValueError, IOError) as e:
        print(e)
        write_csv({}, 'query_responses/results.csv')

if __name__ == "__main__":
    main()