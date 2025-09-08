import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def process_ads_information(data):
    post_views = {}
    video_views = {}

    try:
        ads_and_topics = data['ads_information']['ads_and_topics']
    except KeyError:
        return post_views, video_views

    for file_name, file_data in ads_and_topics.items():
        if file_name == "posts_viewed.json":
            try:
                for entry in file_data['structure']['impressions_history_posts_seen']:
                    author = entry['string_map_data']['Author']['value']
                    post_views[author] = post_views.get(author, 0) + 1
            except KeyError:
                continue

        elif file_name == "videos_watched.json":
            try:
                for entry in file_data['structure']['impressions_history_videos_watched']:
                    author = entry['string_map_data']['Author']['value']
                    video_views[author] = video_views.get(author, 0) + 1
            except KeyError:
                continue

    return post_views, video_views

def generate_csv(post_views, video_views):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        all_accounts = set(post_views.keys()).union(video_views.keys())
        for account in all_accounts:
            writer.writerow({
                'Account': account,
                'Post Views': post_views.get(account, 0),
                'Video Views': video_views.get(account, 0)
            })

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        ads_information_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics')
        ads_information_data = load_json(os.path.join(ads_information_path, 'posts_viewed.json'))
        ads_information_data.update(load_json(os.path.join(ads_information_path, 'videos_watched.json')))
    except FileNotFoundError:
        generate_csv({}, {})
        return

    post_views, video_views = process_ads_information(ads_information_data)
    generate_csv(post_views, video_views)

if __name__ == "__main__":
    main()