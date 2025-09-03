import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file == "posts_viewed.json":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for post in data["impressions_history_posts_seen"]:
                            author = post["string_map_data"]["Author"]["value"]
                            if author not in account_views:
                                account_views[author] = {"Post Views": 0, "Video Views": 0}
                            account_views[author]["Post Views"] += 1
                
                elif file == "videos_watched.json":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for video in data["impressions_history_videos_watched"]:
                            author = video["string_map_data"]["Author"]["value"]
                            if author not in account_views:
                                account_views[author] = {"Post Views": 0, "Video Views": 0}
                            account_views[author]["Video Views"] += 1
        
        return account_views
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON - {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

def save_to_csv(account_views):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ["Account", "Post Views", "Video Views"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account, views in account_views.items():
                writer.writerow({"Account": account, "Post Views": views["Post Views"], "Video Views": views["Video Views"]})
    
    except Exception as e:
        raise ValueError(f"ValueError: Error saving to CSV - {e}")

def main():
    account_views = get_account_views(root_dir)
    save_to_csv(account_views)

if __name__ == "__main__":
    main()