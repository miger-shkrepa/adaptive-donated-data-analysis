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

    posts_data = get_json_data(posts_viewed_file) if os.path.exists(posts_viewed_file) else {}
    videos_data = get_json_data(videos_watched_file) if os.path.exists(videos_watched_file) else {}

    posts_views = {}
    videos_views = {}

    if "impressions_history_posts_seen" in posts_data:
        for entry in posts_data["impressions_history_posts_seen"]:
            author = entry["string_map_data"].get("Author", {}).get("value", "Unknown")
            posts_views[author] = posts_views.get(author, 0) + 1

    if "impressions_history_videos_watched" in videos_data:
        for entry in videos_data["impressions_history_videos_watched"]:
            author = entry["string_map_data"].get("Author", {}).get("value", "Unknown")
            videos_views[author] = videos_views.get(author, 0) + 1

    return posts_views, videos_views

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    posts_views, videos_views = process_ads_and_topics(root_dir)

    # Combine the data into a single dictionary
    combined_data = {}
    for author, count in posts_views.items():
        combined_data[author] = {"Post Views": count, "Video Views": 0}

    for author, count in videos_views.items():
        if author in combined_data:
            combined_data[author]["Video Views"] += count
        else:
            combined_data[author] = {"Post Views": 0, "Video Views": count}

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for account, views in combined_data.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")