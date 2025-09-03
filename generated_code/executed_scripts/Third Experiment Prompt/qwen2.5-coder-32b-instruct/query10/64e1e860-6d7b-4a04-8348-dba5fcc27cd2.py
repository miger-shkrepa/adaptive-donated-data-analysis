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

def process_posts_viewed(data):
    account_views = {}
    if "impressions_history_posts_seen" in data:
        for entry in data["impressions_history_posts_seen"]:
            author = entry["string_map_data"]["Author"]["value"]
            if author in account_views:
                account_views[author] += 1
            else:
                account_views[author] = 1
    return account_views

def process_videos_watched(data):
    account_views = {}
    if "impressions_history_videos_watched" in data:
        for entry in data["impressions_history_videos_watched"]:
            if "Author" in entry["string_map_data"]:
                author = entry["string_map_data"]["Author"]["value"]
                if author in account_views:
                    account_views[author] += 1
                else:
                    account_views[author] = 1
    return account_views

def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Initialize a dictionary to store account views
        account_views = {}

        # Process posts_viewed.json
        posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if os.path.exists(posts_viewed_path):
            posts_viewed_data = get_json_data(posts_viewed_path)
            account_views.update(process_posts_viewed(posts_viewed_data))
        
        # Process videos_watched.json
        videos_watched_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "videos_watched.json")
        if os.path.exists(videos_watched_path):
            videos_watched_data = get_json_data(videos_watched_path)
            account_views.update(process_videos_watched(videos_watched_data))
        
        # Prepare the CSV data
        csv_data = [["Account", "Post Views", "Video Views"]]
        for account, views in account_views.items():
            post_views = 0
            video_views = 0
            if account in account_views:
                if "posts_viewed.json" in posts_viewed_data and account in process_posts_viewed(posts_viewed_data):
                    post_views = process_posts_viewed(posts_viewed_data)[account]
                if "videos_watched.json" in videos_watched_data and account in process_videos_watched(videos_watched_data):
                    video_views = process_videos_watched(videos_watched_data)[account]
            csv_data.append([account, post_views, video_views])
        
        # Write the CSV file
        output_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(csv_data)

    except Exception as e:
        print(f"Error: {str(e)}")
        # Write only the column headers if there's an error
        output_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Account", "Post Views", "Video Views"])

if __name__ == "__main__":
    main()