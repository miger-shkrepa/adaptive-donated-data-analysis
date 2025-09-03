import os
import json
import csv

root_dir = "root_dir"

def find_most_engaged_stories(root):
    user_engagement = {}

    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                if filename == "instagram_profile_information.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for entry in data.get("profile_account_insights", []):
                            string_map_data = entry.get("string_map_data", {})
                            last_story_time = string_map_data.get("Last Story Time", {}).get("value")
                            if last_story_time:
                                user = entry.get("title")
                                if user in user_engagement:
                                    user_engagement[user] += 1
                                else:
                                    user_engagement[user] = 1

    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        print(f"Error: JSON decoding error - {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

    return user_engagement

def save_to_csv(user_engagement):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['User', 'Times Engaged'])
            for user, count in user_engagement.items():
                writer.writerow([user, count])
    except Exception as e:
        print(f"Error: Failed to write CSV - {e}")

if __name__ == "__main__":
    user_engagement = find_most_engaged_stories(root_dir)
    save_to_csv(user_engagement)