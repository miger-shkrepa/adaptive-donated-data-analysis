import os
import json
import csv

root_dir = "root_dir"

def find_viewed_not_liked_accounts(root):
    viewed_accounts = set()
    liked_accounts = set()
    
    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for dirpath, dirnames, filenames in os.walk(root):
            if "recently_viewed_items.json" in filenames:
                with open(os.path.join(dirpath, "recently_viewed_items.json"), 'r') as file:
                    data = json.load(file)
                    for item in data.get("checkout_saved_recently_viewed_products", []):
                        merchant_name = item["string_map_data"]["Merchant Name"]["value"]
                        viewed_accounts.add(merchant_name)
            
            if "liked_posts.json" in filenames:
                with open(os.path.join(dirpath, "liked_posts.json"), 'r') as file:
                    data = json.load(file)
                    for item in data.get("likes_media_likes", []):
                        for post in item["string_list_data"]:
                            liked_accounts.add(post["value"])
            
            if "liked_comments.json" in filenames:
                with open(os.path.join(dirpath, "liked_comments.json"), 'r') as file:
                    data = json.load(file)
                    for item in data.get("likes_comment_likes", []):
                        for comment in item["string_list_data"]:
                            liked_accounts.add(comment["value"])
        
        viewed_not_liked_accounts = viewed_accounts - liked_accounts
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in viewed_not_liked_accounts:
                writer.writerow([account])
    
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise ValueError(f"Error: An unexpected error occurred - {e}")

find_viewed_not_liked_accounts(root_dir)