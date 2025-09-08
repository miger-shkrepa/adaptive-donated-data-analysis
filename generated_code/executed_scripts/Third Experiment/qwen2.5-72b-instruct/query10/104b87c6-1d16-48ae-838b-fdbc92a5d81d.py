import os
import json
import csv

root_dir = "root_dir"

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    accounts_views = {}

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        raise ValueError("Error: JSON file is not properly formatted.")

                    if 'media_metadata' in data:
                        account = os.path.basename(os.path.dirname(file_path))
                        if account not in accounts_views:
                            accounts_views[account] = {'Post Views': 0, 'Video Views': 0}

                        if 'photo_metadata' in data['media_metadata']:
                            accounts_views[account]['Post Views'] += 1
                        elif 'video_metadata' in data['media_metadata']:
                            accounts_views[account]['Video Views'] += 1

    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in accounts_views.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

except Exception as e:
    print(f"An error occurred: {e}")