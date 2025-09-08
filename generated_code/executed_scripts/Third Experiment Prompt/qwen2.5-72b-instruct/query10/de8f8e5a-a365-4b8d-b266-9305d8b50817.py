import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

def process_media_views(data):
    views = {}
    for media_type in ['posts', 'reels', 'stories']:
        media_dir = os.path.join(root_dir, 'media', media_type)
        if not os.path.exists(media_dir):
            continue
        for year_dir in os.listdir(media_dir):
            year_path = os.path.join(media_dir, year_dir)
            if not os.path.isdir(year_path):
                continue
            for file_name in os.listdir(year_path):
                file_path = os.path.join(year_path, file_name)
                if file_name.endswith('.json'):
                    try:
                        json_data = load_json(file_path)
                        if 'ig_stories' in json_data or 'ig_reels_media' in json_data or 'ig_profile_picture' in json_data:
                            for entry in json_data.get(f'ig_{media_type}_media', []):
                                for media in entry.get('media', []):
                                    account = media.get('uri', 'Unknown')
                                    views[account] = views.get(account, 0) + 1
                    except (FileNotFoundError, ValueError) as e:
                        print(f"Error processing {file_path}: {e}")
    return views

def write_csv(views):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, count in views.items():
            writer.writerow({'Account': account, 'Post Views': count, 'Video Views': count})

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        views = process_media_views(root_dir)
        write_csv(views)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()