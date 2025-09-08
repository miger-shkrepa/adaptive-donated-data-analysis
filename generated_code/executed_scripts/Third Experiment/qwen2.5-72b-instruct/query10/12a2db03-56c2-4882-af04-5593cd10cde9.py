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
                if file == "profile_photos.json":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for photo in data.get("ig_profile_picture", []):
                            account = photo.get("title", "Unknown")
                            if account not in account_views:
                                account_views[account] = {"Post Views": 0, "Video Views": 0}
                            account_views[account]["Post Views"] += 1

                if file == "messages.json":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        for message in data.get("messages", []):
                            if "videos" in message:
                                account = message.get("sender_name", "Unknown")
                                if account not in account_views:
                                    account_views[account] = {"Post Views": 0, "Video Views": 0}
                                account_views[account]["Video Views"] += len(message["videos"])

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

    return account_views

def save_to_csv(data, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['Account', 'Post Views', 'Video Views']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account, views in data.items():
                writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

try:
    account_views = process_data(root_dir)
    save_to_csv(account_views, 'query_responses/results.csv')
except Exception as e:
    print(str(e))