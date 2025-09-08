import os
import csv
import json

root_dir = "root_dir"

def load_json_files(root_dir):
    try:
        json_files = {}
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith('.json'):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        json_files[filename] = data
        return json_files
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError("ValueError: Failed to parse JSON: " + str(e))

def extract_user_engagement(json_files):
    user_engagement = {}
    for filename, data in json_files.items():
        if 'story_activities_' in filename:
            for story in data['story_activities_']:
                title = story['title']
                if title not in user_engagement:
                    user_engagement[title] = 0
                user_engagement[title] += 1
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