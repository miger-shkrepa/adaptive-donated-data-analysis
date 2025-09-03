import os
import json
import csv

root_dir = "root_dir"

def extract_accounts(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return [item['value'] for item in data['likes_media_likes']]
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def extract_saved_accounts(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return [item['title'] for item in data['saved_saved_media']]
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def main():
    liked_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
    saved_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'saved', 'saved_posts.json')

    try:
        liked_accounts = extract_accounts(liked_posts_path)
        saved_accounts = extract_saved_accounts(saved_posts_path)

        viewed_not_liked = [account for account in saved_accounts if account not in liked_accounts]

        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in viewed_not_liked:
                writer.writerow([account])

    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])

if __name__ == "__main__":
    main()