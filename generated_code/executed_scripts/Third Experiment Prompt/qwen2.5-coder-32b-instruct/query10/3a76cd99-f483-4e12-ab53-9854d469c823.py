import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

def get_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return eval(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")

def process_ads_and_topics(root_dir):
    posts_viewed = {}
    videos_watched = {}

    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")

    if os.path.exists(posts_viewed_path):
        try:
            data = get_json_data(posts_viewed_path)
            for entry in data.get("impressions_history_posts_seen", []):
                author = entry["string_map_data"]["Author"]["value"]
                posts_viewed[author] = posts_viewed.get(author, 0) + 1
        except Exception as e:
            print(f"Error processing {posts_viewed_path}: {str(e)}")

    if os.path.exists(videos_watched_path):
        try:
            data = get_json_data(videos_watched_path)
            for entry in data.get("impressions_history_videos_watched", []):
                author = entry["string_map_data"]["Author"]["value"]
                videos_watched[author] = videos_watched.get(author, 0) + 1
        except Exception as e:
            print(f"Error processing {videos_watched_path}: {str(e)}")

    return posts_viewed, videos_watched

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    posts_viewed, videos_watched = process_ads_and_topics(root_dir)

    # Aggregate data
    account_data = {}
    for author, count in posts_viewed.items():
        account_data[author] = {"Post Views": count, "Video Views": 0}

    for author, count in videos_watched.items():
        if author in account_data:
            account_data[author]["Video Views"] += count
        else:
            account_data[author] = {"Post Views": 0, "Video Views": count}

    # Write to CSV
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for account, views in account_data.items():
            writer.writerow({'Account': account, 'Post Views': views['Post Views'], 'Video Views': views['Video Views']})

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")