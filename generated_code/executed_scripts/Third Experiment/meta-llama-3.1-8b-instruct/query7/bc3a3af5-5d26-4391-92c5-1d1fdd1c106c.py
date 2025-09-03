import csv
import os

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def extract_story_engagement(data):
    story_engagement = {}
    for post in data['your_instagram_activity']['likes']['liked_posts.json']['structure']['likes_media_likes']:
        for story in post['string_list_data']:
            user = story['value']
            if user not in story_engagement:
                story_engagement[user] = 0
            story_engagement[user] += 1
    return story_engagement

def main():
    try:
        os.chdir(root_dir)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    engagement_data = {}
    for file in os.listdir('.'):
        if file.endswith('.json'):
            data = load_json_file(file)
            engagement_data.update(extract_story_engagement(data))

    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Times Engaged'])
        for user, count in engagement_data.items():
            writer.writerow([user, count])

if __name__ == "__main__":
    main()