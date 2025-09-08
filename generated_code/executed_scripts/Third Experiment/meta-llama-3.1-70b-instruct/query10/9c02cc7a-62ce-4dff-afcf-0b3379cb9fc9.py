import os
import json
import csv

root_dir = "root_dir"

def get_account_views(root_dir):
    account_views = {}
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        for filename in os.listdir(root_dir):
            file_path = os.path.join(root_dir, filename)
            if os.path.isfile(file_path) and filename == "posts_1.json":
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for post in data:
                        if 'media' in post:
                            for media in post['media']:
                                if 'title' in media:
                                    account = media['title']
                                    if account not in account_views:
                                        account_views[account] = {'Post Views': 0, 'Video Views': 0}
                                    account_views[account]['Post Views'] += 1
                                if 'media_metadata' in media and 'photo_metadata' in media['media_metadata']:
                                    if 'exif_data' in media['media_metadata']['photo_metadata']:
                                        for exif in media['media_metadata']['photo_metadata']['exif_data']:
                                            if 'camera_position' in exif:
                                                account = exif['camera_position']
                                                if account not in account_views:
                                                    account_views[account] = {'Post Views': 0, 'Video Views': 0}
                                                account_views[account]['Post Views'] += 1
            elif os.path.isdir(file_path):
                if filename == "202312" or filename == "202401" or filename == "202402":
                    for video_filename in os.listdir(file_path):
                        video_file_path = os.path.join(file_path, video_filename)
                        if os.path.isfile(video_file_path) and video_filename.endswith('.mp4'):
                            account = video_filename.split('_')[0]
                            if account not in account_views:
                                account_views[account] = {'Post Views': 0, 'Video Views': 0}
                            account_views[account]['Video Views'] += 1
    except Exception as e:
        raise ValueError("Error: " + str(e))
    
    return account_views

def save_to_csv(account_views):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Account", "Post Views", "Video Views"])
            for account, views in account_views.items():
                writer.writerow([account, views['Post Views'], views['Video Views']])
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