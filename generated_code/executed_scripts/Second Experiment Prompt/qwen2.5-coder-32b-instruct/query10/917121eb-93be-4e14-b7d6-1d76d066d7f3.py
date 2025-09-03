import os
import csv
import json

# Variable referring to the file input
root_dir = "root_dir"

def get_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while reading the file {file_path}: {e}")

def parse_json_content(json_content):
    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The content is not valid JSON.")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while parsing the JSON content: {e}")

def get_account_views(data, key):
    views = {}
    if key in data:
        for item in data[key]:
            string_map_data = item.get('string_map_data', {})
            author = string_map_data.get('Author', {}).get('value', None)
            if author is not None:
                if author not in views:
                    views[author] = 0
                views[author] += 1
    return views

def main():
    try:
        # Initialize dictionaries to store the views
        post_views = {}
        video_views = {}

        # Path to the posts_viewed.json file
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(posts_viewed_path):
            posts_viewed_content = get_file_content(posts_viewed_path)
            posts_viewed_data = parse_json_content(posts_viewed_content)
            post_views.update(get_account_views(posts_viewed_data, "impressions_history_posts_seen"))

        # Path to the videos_watched.json file
        videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
        if os.path.exists(videos_watched_path):
            videos_watched_content = get_file_content(videos_watched_path)
            videos_watched_data = parse_json_content(videos_watched_content)
            video_views.update(get_account_views(videos_watched_data, "impressions_history_videos_watched"))

        # Prepare the CSV file
        csv_file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Account", "Post Views", "Video Views"])

            # Combine the views from both posts and videos
            all_accounts = set(post_views.keys()).union(set(video_views.keys()))
            for account in all_accounts:
                post_count = post_views.get(account, 0)
                video_count = video_views.get(account, 0)
                csv_writer.writerow([account, post_count, video_count])

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        # Create an empty CSV file with headers if the required files are not found
        csv_file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Account", "Post Views", "Video Views"])
    except ValueError as ve_error:
        print(ve_error)
        # Create an empty CSV file with headers if there is a value error
        csv_file_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Account", "Post Views", "Video Views"])

if __name__ == "__main__":
    main()