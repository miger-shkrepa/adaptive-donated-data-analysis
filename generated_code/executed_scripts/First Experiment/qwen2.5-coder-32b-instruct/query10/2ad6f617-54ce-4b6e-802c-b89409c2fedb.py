import os
import csv
import json

root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def get_account_views(data):
    account_views = {}
    for entry in data:
        author = entry['string_map_data']['Author']['value']
        if author not in account_views:
            account_views[author] = {'Post Views': 0, 'Video Views': 0}
        if 'posts_viewed.json' in file_path:
            account_views[author]['Post Views'] += 1
        elif 'videos_watched.json' in file_path:
            account_views[author]['Video Views'] += 1
    return account_views

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    account_views = {}

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file in ['posts_viewed.json', 'videos_watched.json']:
                file_path = os.path.join(subdir, file)
                data = read_json_file(file_path)
                key = 'impressions_history_posts_seen' if file == 'posts_viewed.json' else 'impressions_history_videos_watched'
                account_views.update(get_account_views(data[key]))

    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in account_views.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

if __name__ == "__main__":
    main()