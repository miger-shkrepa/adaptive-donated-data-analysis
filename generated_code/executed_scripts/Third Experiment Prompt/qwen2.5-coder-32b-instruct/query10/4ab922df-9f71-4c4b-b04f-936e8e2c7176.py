import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

def get_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return eval(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")

def process_ads_and_topics(root_dir):
    ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
    if not os.path.exists(ads_and_topics_dir):
        return {}

    posts_viewed_file = os.path.join(ads_and_topics_dir, "posts_viewed.json")
    videos_watched_file = os.path.join(ads_and_topics_dir, "videos_watched.json")

    posts_viewed_data = get_json_data(posts_viewed_file) if os.path.exists(posts_viewed_file) else {}
    videos_watched_data = get_json_data(videos_watched_file) if os.path.exists(videos_watched_file) else {}

    account_views = {}

    if "impressions_history_posts_seen" in posts_viewed_data:
        for entry in posts_viewed_data["impressions_history_posts_seen"]:
            author = entry["string_map_data"].get("Author", {}).get("value", "Unknown")
            if author not in account_views:
                account_views[author] = {"Post Views": 0, "Video Views": 0}
            account_views[author]["Post Views"] += 1

    if "impressions_history_videos_watched" in videos_watched_data:
        for entry in videos_watched_data["impressions_history_videos_watched"]:
            author = entry["string_map_data"].get("Author", {}).get("value", "Unknown")
            if author not in account_views:
                account_views[author] = {"Post Views": 0, "Video Views": 0}
            account_views[author]["Video Views"] += 1

    return account_views

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    account_views = process_ads_and_topics(root_dir)

    # Ensure the output directory exists
    output_dir = os.path.dirname('query_responses/results.csv')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write the results to a CSV file
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for account, views in account_views.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

if __name__ == "__main__":
    main()