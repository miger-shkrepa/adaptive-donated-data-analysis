import os
import json
import csv

root_dir = "root_dir"

def get_viewed_accounts(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")
        
        liked_accounts = set()
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, 'r') as liked_file:
                liked_data = json.load(liked_file)
                for media_like in liked_data['likes_media_likes']:
                    for string_data in media_like['string_list_data']:
                        liked_accounts.add(string_data['value'])
        
        saved_accounts = set()
        if os.path.exists(saved_posts_path):
            with open(saved_posts_path, 'r') as saved_file:
                saved_data = json.load(saved_file)
                for saved_media in saved_data['saved_saved_media']:
                    saved_accounts.add(saved_media['title'])
        
        viewed_accounts = saved_accounts - liked_accounts
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account'])
            for account in viewed_accounts:
                writer.writerow([account])
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

get_viewed_accounts(root_dir)