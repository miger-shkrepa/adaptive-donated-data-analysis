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
                    raise FileNotFoundError("FileNotFoundError: The file does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file is not a valid JSON.")
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
                    raise FileNotFoundError("FileNotFoundError: The file does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file is not a valid JSON.")
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
                    raise FileNotFoundError("FileNotFoundError: The file does not exist.")
                except json.JSONDecodeError:
                    raise ValueError("Error: The file is not a valid JSON.")
    return accounts

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        viewed_posts = get_viewed_posts(root_dir)
        liked_posts = get_liked_posts(root_dir)
        accounts = get_accounts(root_dir)
        
        not_liked_accounts = accounts - viewed_posts.intersection(liked_posts)
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Account']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account in not_liked_accounts:
                writer.writerow({'Account': account})
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    main()