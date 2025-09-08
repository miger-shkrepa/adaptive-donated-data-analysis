import os
import csv
import json

root_dir = "root_dir"

def get_account_ids(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            account_ids = [item['title'] for item in data['likes_media_likes']]
            return account_ids
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON file.")
    except KeyError:
        raise ValueError("Error: The file does not contain the expected structure.")

def get_viewed_account_ids(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            account_ids = [item['title'] for item in data['ig_stories']]
            return account_ids
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON file.")
    except KeyError:
        raise ValueError("Error: The file does not contain the expected structure.")

def get_unliked_viewed_accounts(root_dir):
    try:
        liked_posts_file_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
        stories_file_path = os.path.join(root_dir, 'your_instagram_activity', 'media', 'stories.json')
        
        liked_account_ids = get_account_ids(liked_posts_file_path) if os.path.exists(liked_posts_file_path) else []
        viewed_account_ids = get_viewed_account_ids(stories_file_path) if os.path.exists(stories_file_path) else []
        
        unliked_viewed_accounts = [account for account in viewed_account_ids if account not in liked_account_ids]
        
        return unliked_viewed_accounts
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(accounts):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Account"])
            for account in accounts:
                writer.writerow([account])
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        unliked_viewed_accounts = get_unliked_viewed_accounts(root_dir)
        save_to_csv(unliked_viewed_accounts)
    except Exception as e:
        print(f"Error: {str(e)}")
        save_to_csv([])

if __name__ == "__main__":
    main()