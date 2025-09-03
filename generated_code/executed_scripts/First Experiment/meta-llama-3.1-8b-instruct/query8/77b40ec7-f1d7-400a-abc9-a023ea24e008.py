import os
import csv
import json

root_dir = "root_dir"

def load_json_files(root_dir):
    data = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data.append(json.load(f))
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON file: {file_path}")
                except FileNotFoundError as e:
                    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    return data

def extract_user_interactions(data):
    user_interactions = {}
    for item in data:
        if 'likes' in item:
            for file in item['likes']:
                if file['type'] == 'json':
                    for interaction in file['structure']['likes_media_likes']:
                        user = interaction['title']
                        if user not in user_interactions:
                            user_interactions[user] = {'post_likes': 0, 'story_likes': 0, 'comments': 0}
                        user_interactions[user]['post_likes'] += len(interaction['string_list_data'])
                    for file in item['likes']:
                        if file['type'] == 'json':
                            for interaction in file['structure']['likes_comment_likes']:
                                user = interaction['title']
                                if user not in user_interactions:
                                    user_interactions[user] = {'post_likes': 0, 'story_likes': 0, 'comments': 0}
                                user_interactions[user]['comments'] += len(interaction['string_list_data'])
    return user_interactions

def save_to_csv(user_interactions, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, interactions in user_interactions.items():
            writer.writerow({'User': user, 'Post Likes': interactions['post_likes'], 'Story Likes': 0, 'Comments': interactions['comments']})

def main():
    try:
        data = load_json_files(root_dir)
        user_interactions = extract_user_interactions(data)
        save_to_csv(user_interactions, 'query_responses/results.csv')
    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()