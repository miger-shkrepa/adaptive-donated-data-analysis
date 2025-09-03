import os
import json
import csv

root_dir = "root_dir"

def get_story_engagement(user_data):
    story_engagement = {}
    for file_name in os.listdir(os.path.join(root_dir, "personal_information")):
        if file_name == "instagram_profile_information.json":
            file_path = os.path.join(root_dir, "personal_information", file_name)
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for entry in data.get("profile_account_insights", []):
                        string_map_data = entry.get("string_map_data", {})
                        for key, value in string_map_data.items():
                            if "Story" in key and "Time" in key:
                                user = value.get("value", "")
                                if user:
                                    story_engagement[user] = story_engagement.get(user, 0) + 1
            except FileNotFoundError:
                raise FileNotFoundError("Error: The specified JSON file does not exist.")
            except json.JSONDecodeError:
                raise ValueError("Error: The JSON file is not properly formatted.")
            except Exception as e:
                raise Exception(f"Error: An unexpected error occurred: {str(e)}")
    return story_engagement

def write_to_csv(story_engagement):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, count in story_engagement.items():
                writer.writerow({'User': user, 'Times Engaged': count})
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV: {str(e)}")

if __name__ == "__main__":
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    story_engagement = get_story_engagement(root_dir)
    write_to_csv(story_engagement)