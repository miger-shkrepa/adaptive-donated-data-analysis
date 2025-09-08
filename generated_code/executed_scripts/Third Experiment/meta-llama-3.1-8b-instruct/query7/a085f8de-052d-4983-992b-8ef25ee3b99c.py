import csv
import os

root_dir = "root_dir"

def get_user_engagement(root_dir):
    user_engagement = {}
    for user in os.listdir(root_dir):
        user_path = os.path.join(root_dir, user)
        if os.path.isdir(user_path):
            for file in os.listdir(user_path):
                file_path = os.path.join(user_path, file)
                if file.endswith(".json"):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if 'story_activities_story_likes' in data['structure']:
                            for story in data['structure']['story_activities_story_likes']:
                                for like in story['string_list_data']:
                                    user_engagement[user] = user_engagement.get(user, 0) + 1
    return user_engagement

def write_to_csv(user_engagement, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
        for user, engagement in user_engagement.items():
            writer.writerow([user, engagement])

try:
    root_dir = os.path.abspath(root_dir)
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    user_engagement = get_user_engagement(root_dir)
    write_to_csv(user_engagement, 'query_responses/results.csv')
except FileNotFoundError as e:
    raise e
except Exception as e:
    raise ValueError("ValueError: An error occurred while processing the data.")