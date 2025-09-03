import os
import json
import csv

root_dir = "root_dir"

def get_story_engagement(user_data_dir):
    story_engagement = {}
    try:
        if not os.path.exists(user_data_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        personal_info_path = os.path.join(user_data_dir, "personal_information", "instagram_profile_information.json")
        if not os.path.exists(personal_info_path):
            return story_engagement

        with open(personal_info_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("profile_account_insights", []):
                string_map_data = entry.get("string_map_data", {})
                for key, value in string_map_data.items():
                    if "Story" in key and "Time" in key:
                        user = value.get("value", "")
                        if user:
                            story_engagement[user] = story_engagement.get(user, 0) + 1

    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

    return story_engagement

def write_to_csv(story_engagement):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
        for user, count in story_engagement.items():
            writer.writerow([user, count])

try:
    story_engagement = get_story_engagement(root_dir)
    write_to_csv(story_engagement)
except Exception as e:
    print(e)