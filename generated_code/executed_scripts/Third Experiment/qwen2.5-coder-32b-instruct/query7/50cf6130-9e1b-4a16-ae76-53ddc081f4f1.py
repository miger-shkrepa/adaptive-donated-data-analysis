import os
import csv
import json

root_dir = "root_dir"

def get_story_engagement_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")
    
    engagement_data = {}
    for item in data.get('story_activities_story_likes', []) + data.get('story_activities_reaction_sticker_reactions', []):
        for entry in item.get('string_list_data', []):
            user = entry.get('value')
            if user:
                engagement_data[user] = engagement_data.get(user, 0) + 1
    return engagement_data

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_likes_path = os.path.join(root_dir, 'story_likes.json')
        story_reaction_sticker_reactions_path = os.path.join(root_dir, 'story_reaction_sticker_reactions.json')
        
        engagement_data = {}
        
        if os.path.exists(story_likes_path):
            engagement_data.update(get_story_engagement_data(story_likes_path))
        
        if os.path.exists(story_reaction_sticker_reactions_path):
            engagement_data.update(get_story_engagement_data(story_reaction_sticker_reactions_path))
        
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            for user, times in engagement_data.items():
                writer.writerow([user, times])
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()