import os
import json
import csv

root_dir = "root_dir"

def get_viewed_accounts():
    viewed_accounts = set()
    liked_accounts = set()
    
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check for viewed posts
        viewed_posts_path = os.path.join(root_dir, "activity", "viewed_posts.json")
        if os.path.exists(viewed_posts_path):
            with open(viewed_posts_path, 'r') as file:
                data = json.load(file)
                for entry in data.get("viewed_posts", []):
                    account = entry.get("string_map_data", {}).get("Account", {}).get("value")
                    if account:
                        viewed_accounts.add(account)
        else:
            print("Warning: viewed_posts.json not found. Assuming no viewed posts.")
        
        # Check for liked posts
        liked_posts_path = os.path.join(root_dir, "activity", "liked_posts.json")
        if os.path.exists(liked_posts_path):
            with open(liked_posts_path, 'r') as file:
                data = json.load(file)
                for entry in data.get("liked_posts", []):
                    account = entry.get("string_map_data", {}).get("Account", {}).get("value")
                    if account:
                        liked_accounts.add(account)
        else:
            print("Warning: liked_posts.json not found. Assuming no liked posts.")
        
        # Find accounts viewed but not liked
        accounts_viewed_not_liked = viewed_accounts - liked_accounts
        
        return accounts_viewed_not_liked
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(accounts):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account"])
        for account in accounts:
            writer.writerow([account])

try:
    accounts_viewed_not_liked = get_viewed_accounts()
    write_to_csv(accounts_viewed_not_liked)
except Exception as e:
    print(e)