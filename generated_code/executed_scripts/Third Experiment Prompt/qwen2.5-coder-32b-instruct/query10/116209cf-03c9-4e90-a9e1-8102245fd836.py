import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

def get_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            import json
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def process_posts_views(data):
    account_views = {}
    if 'impressions_history_posts_seen' in data:
        for entry in data['impressions_history_posts_seen']:
            author = entry['string_map_data']['Author']['value']
            if author in account_views:
                account_views[author] += 1
            else:
                account_views[author] = 1
    return account_views

def process_videos_watched(data):
    account_views = {}
    if 'impressions_history_videos_watched' in data:
        for entry in data['impressions_history_videos_watched']:
            author = entry['string_map_data']['Author']['value']
            if author in account_views:
                account_views[author] += 1
            else:
                account_views[author] = 1
    return account_views

def aggregate_views(post_views, video_views):
    combined_views = {}
    for account, views in post_views.items():
        combined_views[account] = views
    for account, views in video_views.items():
        if account in combined_views:
            combined_views[account] += views
        else:
            combined_views[account] = views
    return combined_views

def main():
    try:
        # Check if the root directory exists
        if not os.path.isdir(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Initialize dictionaries to store views
        post_views = {}
        video_views = {}

        # Process posts_viewed.json
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(posts_viewed_path):
            posts_data = get_json_data(posts_viewed_path)
            post_views = process_posts_views(posts_data)

        # Process videos_watched.json
        videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
        if os.path.exists(videos_watched_path):
            videos_data = get_json_data(videos_watched_path)
            video_views = process_videos_watched(videos_data)

        # Aggregate views
        combined_views = aggregate_views(post_views, video_views)

        # Prepare CSV data
        csv_data = [['Account', 'Post Views', 'Video Views']]
        for account, total_views in combined_views.items():
            post_count = post_views.get(account, 0)
            video_count = video_views.get(account, 0)
            csv_data.append([account, post_count, video_count])

        # Write CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(csv_data)

    except Exception as e:
        print(f"Error: {e}")
        # Write only the column headers if an error occurs
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Account', 'Post Views', 'Video Views'])

if __name__ == "__main__":
    main()