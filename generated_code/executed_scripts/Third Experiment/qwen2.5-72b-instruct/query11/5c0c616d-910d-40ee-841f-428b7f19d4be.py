import os
import json
import csv

root_dir = "root_dir"

def get_viewed_accounts():
    try:
        viewed_accounts = set()
        liked_accounts = set()
        
        ads_info_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if not os.path.exists(ads_info_path):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
        
        with open(ads_info_path, 'r') as file:
            data = json.load(file)
            for post in data.get("impressions_history_posts_seen", []):
                author = post.get("string_map_data", {}).get("Author", {}).get("value")
                if author:
                    viewed_accounts.add(author)
        
        likes_path = os.path.join(root_dir, "media", "posts")
        if not os.path.exists(likes_path):
            raise FileNotFoundError("FileNotFoundError: The posts directory does not exist.")
        
        for year_month in os.listdir(likes_path):
            year_month_path = os.path.join(likes_path, year_month)
            if os.path.isdir(year_month_path):
                for file in os.listdir(year_month_path):
                    if file.endswith(".json"):
                        with open(os.path.join(year_month_path, file), 'r') as like_file:
                            like_data = json.load(like_file)
                            liked_author = like_data.get("string_map_data", {}).get("Author", {}).get("value")
                            if liked_author:
                                liked_accounts.add(liked_author)
        
        accounts_viewed_not_liked = viewed_accounts - liked_accounts
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
            for account in accounts_viewed_not_liked:
                writer.writerow([account])
        
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Account"])
    except Exception as e:
        raise ValueError(f"Error: An unexpected error occurred: {str(e)}")

get_viewed_accounts()