import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    user_engagement = {}
    
    # Check if root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if 'story_likes.json' file exists
    story_likes_path = os.path.join(root_dir, 'story_likes.json')
    if not os.path.exists(story_likes_path):
        return user_engagement
    
    # Load 'story_likes.json' file
    try:
        with open(story_likes_path, 'r') as file:
            story_likes_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to parse 'story_likes.json' file.")
    
    # Extract user engagement data
    for story_like in story_likes_data['story_activities_story_likes']:
        title = story_like['title']
        if title not in user_engagement:
            user_engagement[title] = 0
        user_engagement[title] += len(story_like['string_list_data'])
    
    return user_engagement

def save_to_csv(user_engagement):
    csv_path = 'query_responses/results.csv'
    csv_dir = os.path.dirname(csv_path)
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User', 'Times Engaged'])
        for user, engagement in user_engagement.items():
            writer.writerow([user, engagement])

def main():
    try:
        user_engagement = get_user_engagement(root_dir)
        save_to_csv(user_engagement)
    except Exception as e:
        print(f"Error: {str(e)}")
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['User', 'Times Engaged'])

if __name__ == "__main__":
    main()