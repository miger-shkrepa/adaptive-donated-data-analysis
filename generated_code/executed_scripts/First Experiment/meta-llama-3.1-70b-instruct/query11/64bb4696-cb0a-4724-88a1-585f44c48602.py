import os
import json
import csv

root_dir = "root_dir"

def get_viewed_posts(root_dir):
    viewed_posts = set()
    for root, dirs, files in os.walk(os.path.join(root_dir, 'media')):
        for file in files:
            if file == 'posts_1.json':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for post in data['media']:
                            viewed_posts.add(post['title'])
                except FileNotFoundError:
                    raise FileNotFoundError("FileNotFoundError: The file {} does not exist.".format(file_path))
                except json.JSONDecodeError:
                    raise ValueError("Error: The file {} is not a valid JSON file.".format(file_path))
    return viewed_posts

def get_liked_posts(root_dir):
    liked_posts = set()
    for root, dirs, files in os.walk(os.path.join(root_dir, 'likes')):
        for file in files:
            if file == 'liked_posts.json':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for post in data['likes_media_likes']:
                            liked_posts.add(post['title'])
                except FileNotFoundError:
                    raise FileNotFoundError("FileNotFoundError: The file {} does not exist.".format(file_path))
                except json.JSONDecodeError:
                    raise ValueError("Error: The file {} is not a valid JSON file.".format(file_path))
    return liked_posts

def get_accounts(root_dir):
    accounts = set()
    for root, dirs, files in os.walk(os.path.join(root_dir, 'messages', 'inbox')):
        for file in files:
            if file.startswith('message_') and file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for participant in data['participants']:
                            accounts.add(participant['name'])
                except FileNotFoundError:
                    raise FileNotFoundError("FileNotFoundError: The file {} does not exist.".format(file_path))
                except json.JSONDecodeError:
                    raise ValueError("Error: The file {} is not a valid JSON file.".format(file_path))
    return accounts

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    viewed_posts = get_viewed_posts(root_dir)
    liked_posts = get_liked_posts(root_dir)
    accounts = get_accounts(root_dir)
    
    result = []
    for account in accounts:
        if account in viewed_posts and account not in liked_posts:
            result.append([account])
    
    with open('query_responses/results.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Account'])
        writer.writerows(result)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error: {}".format(str(e)))