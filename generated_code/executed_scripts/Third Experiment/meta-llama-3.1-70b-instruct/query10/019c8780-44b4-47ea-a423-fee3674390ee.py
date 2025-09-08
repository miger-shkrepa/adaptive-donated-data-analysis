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
                if file_name == "story_likes.json":
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for activity in data["story_activities_story_likes"]:
                            title = activity["title"]
                            if title not in account_views:
                                account_views[title] = {"Post Views": 0, "Video Views": 0}
                            account_views[title]["Post Views"] += len(activity["string_list_data"])
                
                elif file_name == "liked_posts.json":
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for like in data["likes_media_likes"]:
                            title = like["title"]
                            if title not in account_views:
                                account_views[title] = {"Post Views": 0, "Video Views": 0}
                            account_views[title]["Post Views"] += len(like["string_list_data"])
                
                elif file_name == "liked_comments.json":
                    file_path = os.path.join(dir_path, file_name)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for like in data["likes_comment_likes"]:
                            title = like["title"]
                            if title not in account_views:
                                account_views[title] = {"Post Views": 0, "Video Views": 0}
                            account_views[title]["Post Views"] += len(like["string_list_data"])
        
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
    try:
        account_views = get_account_views(root_dir)
        if not account_views:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Account", "Post Views", "Video Views"])
        else:
            save_to_csv(account_views)
    
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()