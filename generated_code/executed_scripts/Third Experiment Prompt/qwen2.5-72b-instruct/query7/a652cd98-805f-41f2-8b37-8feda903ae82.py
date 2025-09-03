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
    story_engagement = {}
    
    if 'story_activities_emoji_quick_reactions' in data:
        for entry in data['story_activities_emoji_quick_reactions']:
            for item in entry['string_list_data']:
                media_owner = item['value']
                if media_owner in story_engagement:
                    story_engagement[media_owner] += 1
                else:
                    story_engagement[media_owner] = 1
    
    if 'story_activities_story_likes' in data:
        for entry in data['story_activities_story_likes']:
            for item in entry['string_list_data']:
                if 'value' in item:
                    media_owner = item['value']
                    if media_owner in story_engagement:
                        story_engagement[media_owner] += 1
                    else:
                        story_engagement[media_owner] = 1
    
    return story_engagement

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_interactions_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'emoji_story_reactions.json')
        story_likes_path = os.path.join(root_dir, 'your_instagram_activity', 'story_interactions', 'story_likes.json')
        
        story_interactions_data = {}
        story_likes_data = {}
        
        if os.path.exists(story_interactions_path):
            story_interactions_data = load_json_file(story_interactions_path)
        
        if os.path.exists(story_likes_path):
            story_likes_data = load_json_file(story_likes_path)
        
        story_engagement = process_story_interactions(story_interactions_data)
        story_engagement.update(process_story_interactions(story_likes_data))
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            if story_engagement:
                for user, count in story_engagement.items():
                    writer.writerow({'User': user, 'Times Engaged': count})
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()