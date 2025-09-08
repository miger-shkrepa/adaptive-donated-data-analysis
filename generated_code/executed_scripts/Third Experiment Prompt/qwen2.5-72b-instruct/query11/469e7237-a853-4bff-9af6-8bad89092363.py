import os
import json
import csv

root_dir = "root_dir"

def get_viewed_accounts(root_dir):
    viewed_accounts = set()
    try:
        ads_and_topics_path = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if os.path.exists(ads_and_topics_path):
            posts_viewed_path = os.path.join(ads_and_topics_path, "posts_viewed.json")
            if os.path.exists(posts_viewed_path):
                with open(posts_viewed_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for entry in data.get("impressions_history_posts_seen", []):
                        string_map_data = entry.get("string_map_data", {})
                        author = string_map_data.get("Author", {}).get("value")
                        if author:
                            viewed_accounts.add(author)
    except Exception as e:
        raise ValueError(f"Error: Failed to process posts_viewed.json - {str(e)}")
    return viewed_accounts

def get_liked_accounts(root_dir):
    liked_accounts = set()
    try:
        likes_path = os.path.join(root_dir, "your_instagram_activity", "likes")
        if os.path.exists(likes_path):
            liked_posts_path = os.path.join(likes_path, "liked_posts.json")
            if os.path.exists(liked_posts_path):
                with open(liked_posts_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    for entry in data.get("likes_media_likes", []):
                        string_list_data = entry.get("string_list_data", [])
                        for item in string_list_data:
                            liked_accounts.add(item.get("value", ""))
    except Exception as e:
        raise ValueError(f"Error: Failed to process liked_posts.json - {str(e)}")
    return liked_accounts

def find_accounts_viewed_not_liked(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    viewed_accounts = get_viewed_accounts(root_dir)
    liked_accounts = get_liked_accounts(root_dir)
    
    accounts_viewed_not_liked = viewed_accounts - liked_accounts
    
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Account'])
        for account in accounts_viewed_not_liked:
            writer.writerow([account])

# Execute the function
try:
    find_accounts_viewed_not_liked(root_dir)
except Exception as e:
    print(str(e))