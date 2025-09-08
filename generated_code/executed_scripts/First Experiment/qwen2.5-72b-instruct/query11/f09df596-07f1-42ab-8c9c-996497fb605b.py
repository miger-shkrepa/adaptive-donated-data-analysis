import os
import json
import csv

root_dir = "root_dir"

def find_viewed_not_liked_accounts(root):
    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        viewed_accounts = set()
        liked_accounts = set()
        
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                if filename == "posts_1.json":
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for post in data.get("media", []):
                            title = post.get("title")
                            if title:
                                viewed_accounts.add(title)
                
                if filename == "liked_posts.json":
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for like in data.get("likes_media_likes", []):
                            for item in like.get("string_list_data", []):
                                liked_accounts.add(item.get("value"))
        
        accounts_viewed_not_liked = viewed_accounts - liked_accounts
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts_viewed_not_liked:
                writer.writerow([account])
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

try:
    find_viewed_not_liked_accounts(root_dir)
except Exception as e:
    print(e)