import os
import csv
import json

root_dir = "root_dir"

def load_json_files(root_dir):
    try:
        json_files = {}
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                if file_name.endswith('.json'):
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        json_data = json.load(file)
                        json_files[file_name] = json_data
        return json_files
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError("ValueError: Failed to parse JSON file: " + str(e))

def extract_user_engagement(json_files):
    user_engagement = {}
    for file_name, json_data in json_files.items():
        if 'story_activities_' in file_name:
            for story in json_data['structure'][file_name.split('.')[0].split('_')[-1]]:
                user_id = story['title']
                if user_id not in user_engagement:
                    user_engagement[user_id] = 0
                user_engagement[user_id] += 1
    return user_engagement

def save_to_csv(user_engagement):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
        for user, times_engaged in user_engagement.items():
            writer.writerow([user, times_engaged])

def main():
    json_files = load_json_files(root_dir)
    user_engagement = extract_user_engagement(json_files)
    save_to_csv(user_engagement)

if __name__ == "__main__":
    main()