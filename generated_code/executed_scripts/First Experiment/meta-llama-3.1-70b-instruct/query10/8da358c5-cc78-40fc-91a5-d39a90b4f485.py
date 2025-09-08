import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                if file_name == "posts_viewed.json":
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for post in data["impressions_history_posts_seen"]:
                            author = post["string_map_data"]["Author"]["value"]
                            if author not in account_views:
                                account_views[author] = {"Post Views": 0, "Video Views": 0}
                            account_views[author]["Post Views"] += 1
                
                elif file_name == "videos_watched.json":
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for video in data["impressions_history_videos_watched"]:
                            author = video["string_map_data"]["Author"]["value"]
                            if author not in account_views:
                                account_views[author] = {"Post Views": 0, "Video Views": 0}
                            account_views[author]["Video Views"] += 1
        
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
    save_to_csv(account_views)

if __name__ == "__main__":
    main()