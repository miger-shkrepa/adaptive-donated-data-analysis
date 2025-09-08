import os
import json
import csv

root_dir = "root_dir"

def process_data():
    post_views = {}
    video_views = {}

    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        ads_info_path = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_info_path):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")

        # Process posts_viewed.json
        posts_viewed_path = os.path.join(ads_info_path, "posts_viewed.json")
        if os.path.exists(posts_viewed_path):
            with open(posts_viewed_path, 'r') as file:
                data = json.load(file)
                for item in data.get("impressions_history_posts_seen", []):
                    author = item["string_map_data"]["Author"]["value"]
                    if author in post_views:
                        post_views[author] += 1
                    else:
                        post_views[author] = 1
        else:
            print("Warning: posts_viewed.json does not exist. Post views will be treated as 0.")

        # Process videos_watched.json
        videos_watched_path = os.path.join(ads_info_path, "videos_watched.json")
        if os.path.exists(videos_watched_path):
            with open(videos_watched_path, 'r') as file:
                data = json.load(file)
                for item in data.get("impressions_history_videos_watched", []):
                    author = item["string_map_data"]["Author"]["value"]
                    if author in video_views:
                        video_views[author] += 1
                    else:
                        video_views[author] = 1
        else:
            print("Warning: videos_watched.json does not exist. Video views will be treated as 0.")

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise ValueError(f"Error: An unexpected error occurred - {e}")

    return post_views, video_views

def write_to_csv(post_views, video_views):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        all_accounts = set(list(post_views.keys()) + list(video_views.keys()))
        for account in all_accounts:
            post_view_count = post_views.get(account, 0)
            video_view_count = video_views.get(account, 0)
            writer.writerow({'Account': account, 'Post Views': post_view_count, 'Video Views': video_view_count})

def main():
    try:
        post_views, video_views = process_data()
        write_to_csv(post_views, video_views)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()