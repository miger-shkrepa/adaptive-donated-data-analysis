import os
import json
import csv

root_dir = "root_dir"

def get_story_engagement(root):
    user_engagement = {}
    story_likes_path = os.path.join(root, "story_interactions", "story_likes.json")
    
    if not os.path.exists(root):
        raise FileNotFoundError("Error: The root directory does not exist.")
    
    if not os.path.exists(story_likes_path):
        return user_engagement
    
    try:
        with open(story_likes_path, 'r') as file:
            data = json.load(file)
            story_activities = data.get("story_activities_story_likes", [])
            
            for activity in story_activities:
                title = activity.get("title")
                if title:
                    user_engagement[title] = user_engagement.get(title, 0) + 1
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    
    return user_engagement

def write_to_csv(data, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
        for user, count in data.items():
            writer.writerow([user, count])

try:
    engagement_data = get_story_engagement(root_dir)
    write_to_csv(engagement_data, 'query_responses/results.csv')
except Exception as e:
    print(e)