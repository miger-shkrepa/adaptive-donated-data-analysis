import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        your_instagram_activity_dir = os.path.join(root_dir, "your_instagram_activity")
        if not os.path.exists(your_instagram_activity_dir):
            return account_views
        
        likes_dir = os.path.join(your_instagram_activity_dir, "likes")
        if os.path.exists(likes_dir):
            liked_posts_json_path = os.path.join(likes_dir, "liked_posts.json")
            if os.path.exists(liked_posts_json_path):
                with open(liked_posts_json_path, 'r') as file:
                    liked_posts_data = json.load(file)
                    for post in liked_posts_data["likes_media_likes"]:
                        for data in post["string_list_data"]:
                            account = data["href"].split("/")[-2]
                            if account not in account_views:
                                account_views[account] = {"Post Views": 0, "Video Views": 0}
                            account_views[account]["Post Views"] += 1
        
        saved_dir = os.path.join(your_instagram_activity_dir, "saved")
        if os.path.exists(saved_dir):
            saved_posts_json_path = os.path.join(saved_dir, "saved_posts.json")
            if os.path.exists(saved_posts_json_path):
                with open(saved_posts_json_path, 'r') as file:
                    saved_posts_data = json.load(file)
                    for post in saved_posts_data["saved_saved_media"]:
                        account = post["string_map_data"]["Saved on"]["href"].split("/")[-2]
                        if account not in account_views:
                            account_views[account] = {"Post Views": 0, "Video Views": 0}
                        account_views[account]["Post Views"] += 1
        
        return account_views
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(account_views):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Post Views", "Video Views"])
            for account, views in account_views.items():
                writer.writerow([account, views["Post Views"], views["Video Views"]])
    
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    account_views = get_account_views(root_dir)
    if not account_views:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Post Views", "Video Views"])
    else:
        save_to_csv(account_views)

if __name__ == "__main__":
    main()