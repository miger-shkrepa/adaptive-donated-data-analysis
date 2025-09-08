import os
import json
import csv

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The specified JSON file is not properly formatted.")

def process_story_likes(data):
    user_engagement = {}
    try:
        story_activities = data.get("story_activities_story_likes", [])
        for activity in story_activities:
            string_list_data = activity.get("string_list_data", [])
            for entry in string_list_data:
                if "value" in entry:
                    user = entry["value"]
                    user_engagement[user] = user_engagement.get(user, 0) + 1
    except Exception as e:
        raise ValueError(f"Error: Failed to process story likes data. {str(e)}")
    return user_engagement

def write_csv(results, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["User", "Times Engaged"])
            for user, count in results.items():
                writer.writerow([user, count])
    except Exception as e:
        raise ValueError(f"Error: Failed to write CSV file. {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        story_likes_path = os.path.join(root_dir, "your_instagram_activity", "story_interactions", "story_likes.json")
        if not os.path.exists(story_likes_path):
            write_csv({}, 'query_responses/results.csv')
            return
        
        story_likes_data = load_json_file(story_likes_path)
        user_engagement = process_story_likes(story_likes_data)
        
        write_csv(user_engagement, 'query_responses/results.csv')
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()