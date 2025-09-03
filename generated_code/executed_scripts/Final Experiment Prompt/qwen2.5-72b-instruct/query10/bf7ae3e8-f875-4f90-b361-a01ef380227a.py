import json
import os
import csv

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def count_views(data, key):
    view_counts = {}
    if key in data:
        for entry in data[key]:
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                view_counts[author] = view_counts.get(author, 0) + 1
    return view_counts

def process_data(posts_file, videos_file):
    post_views = {}
    video_views = {}

    if os.path.exists(posts_file):
        posts_data = load_json_data(posts_file)
        post_views = count_views(posts_data, "impressions_history_posts_seen")
    else:
        print("Warning: posts_viewed.json not found. Post views will be set to 0.")

    if os.path.exists(videos_file):
        videos_data = load_json_data(videos_file)
        video_views = count_views(videos_data, "impressions_history_videos_watched")
    else:
        print("Warning: videos_watched.json not found. Video views will be set to 0.")

    return post_views, video_views

def merge_views(post_views, video_views):
    all_accounts = set(list(post_views.keys()) + list(video_views.keys()))
    merged_views = []

    for account in all_accounts:
        post_view_count = post_views.get(account, 0)
        video_view_count = video_views.get(account, 0)
        merged_views.append([account, post_view_count, video_view_count])

    return merged_views

def save_to_csv(data, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Account", "Post Views", "Video Views"])
        csvwriter.writerows(data)

def main():
    posts_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    try:
        post_views, video_views = process_data(posts_file, videos_file)
        merged_views = merge_views(post_views, video_views)
        save_to_csv(merged_views, 'query_responses/results.csv')
    except Exception as e:
        print(f"Error: {e}")
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Account", "Post Views", "Video Views"])

if __name__ == "__main__":
    main()