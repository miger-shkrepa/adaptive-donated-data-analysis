import os
import csv
import json

root_dir = "root_dir"

def get_story_likes_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('story_activities_story_likes', [])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The story_likes.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The story_likes.json file is not a valid JSON file.")

def aggregate_story_likes(story_likes_data):
    engagement_count = {}
    for entry in story_likes_data:
        title = entry.get('title')
        if title:
            engagement_count[title] = engagement_count.get(title, 0) + 1
    return engagement_count

def main():
    story_likes_path = os.path.join(root_dir, 'story_interactions', 'story_likes.json')
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(story_likes_path):
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
        return
    
    story_likes_data = get_story_likes_data(story_likes_path)
    engagement_count = aggregate_story_likes(story_likes_data)
    
    sorted_engagement = sorted(engagement_count.items(), key=lambda x: x[1], reverse=True)
    
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
        for user, count in sorted_engagement:
            writer.writerow([user, count])

if __name__ == "__main__":
    main()