import os
import json
import csv

root_dir = "root_dir"

def process_story_engagement(root):
    user_engagement = {}
    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_likes_path = os.path.join(root, "story_interactions", "story_likes.json")
        if os.path.exists(story_likes_path):
            with open(story_likes_path, 'r') as file:
                data = json.load(file)
                for item in data.get("story_activities_story_likes", []):
                    title = item.get("title")
                    if title:
                        user_engagement[title] = user_engagement.get(title, 0) + len(item.get("string_list_data", []))
        else:
            print("Warning: story_likes.json not found. Contributions from this file will be treated as 0.")
        
        # Additional story engagement files can be processed similarly if they exist.
        
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")
    
    return user_engagement

def save_to_csv(data, path):
    try:
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
            for user, count in data.items():
                writer.writerow([user, count])
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        user_engagement = process_story_engagement(root_dir)
        save_to_csv(user_engagement, 'query_responses/results.csv')
    except Exception as e:
        print(e)