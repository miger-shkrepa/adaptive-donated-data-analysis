import os
import json
import csv

root_dir = "root_dir"

def process_data(directory):
    account_views = {}
    try:
        if not os.path.exists(directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == "recently_viewed_items.json":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for item in data.get("checkout_saved_recently_viewed_products", []):
                            merchant_name = item["string_map_data"]["Merchant Name"]["value"]
                            if merchant_name not in account_views:
                                account_views[merchant_name] = {"Post Views": 0, "Video Views": 0}
                            account_views[merchant_name]["Post Views"] += 1

                if file == "liked_posts.json":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for item in data.get("likes_media_likes", []):
                            for entry in item["string_list_data"]:
                                if "value" in entry:
                                    account_name = entry["value"]
                                    if account_name not in account_views:
                                        account_views[account_name] = {"Post Views": 0, "Video Views": 0}
                                    account_views[account_name]["Post Views"] += 1

                if file == "liked_comments.json":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for item in data.get("likes_comment_likes", []):
                            for entry in item["string_list_data"]:
                                if "value" in entry:
                                    account_name = entry["value"]
                                    if account_name not in account_views:
                                        account_views[account_name] = {"Post Views": 0, "Video Views": 0}
                                    account_views[account_name]["Post Views"] += 1

        return account_views

    except json.JSONDecodeError:
        raise ValueError("Error: JSON data is not properly formatted.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(data):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        if not data:
            return
        for account, views in data.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

try:
    account_views = process_data(root_dir)
    write_to_csv(account_views)
except Exception as e:
    print(e)