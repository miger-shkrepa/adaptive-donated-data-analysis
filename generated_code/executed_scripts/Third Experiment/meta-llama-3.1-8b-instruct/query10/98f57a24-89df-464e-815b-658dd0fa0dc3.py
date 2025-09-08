import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize variables to store the data
account_views = {}
video_views = {}

# Function to parse JSON files
def parse_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            return eval(data)
    except Exception as e:
        print(f"Error parsing JSON file: {e}")
        return None

# Function to extract data from JSON files
def extract_data(data):
    if data is None:
        return None
    if "story_likes.json" in data and "story_activities_story_likes" in data["story_likes.json"]["structure"]:
        for item in data["story_likes.json"]["structure"]["story_activities_story_likes"]:
            if "string_list_data" in item and len(item["string_list_data"]) > 0:
                for item2 in item["string_list_data"]:
                    if "timestamp" in item2:
                        account = item["title"]
                        views = item2["timestamp"]
                        if account in account_views:
                            account_views[account] += views
                        else:
                            account_views[account] = views
    if "posts_viewed.json" in data and "impressions_history_posts_seen" in data["posts_viewed.json"]["structure"]:
        for item in data["posts_viewed.json"]["structure"]["impressions_history_posts_seen"]:
            if "string_map_data" in item and "Time" in item["string_map_data"]:
                account = "Posts"
                views = item["string_map_data"]["Time"]["timestamp"]
                if account in account_views:
                    account_views[account] += views
                else:
                    account_views[account] = views
    if "videos_watched.json" in data and "impressions_history_videos_watched" in data["videos_watched.json"]["structure"]:
        for item in data["videos_watched.json"]["structure"]["impressions_history_videos_watched"]:
            if "string_map_data" in item and "Time" in item["string_map_data"]:
                account = "Videos"
                views = item["string_map_data"]["Time"]["timestamp"]
                if account in account_views:
                    account_views[account] += views
                else:
                    account_views[account] = views
    if "accounts_you've_favorited.json" in data and "relationships_feed_favorites" in data["accounts_you've_favorited.json"]["structure"]:
        for item in data["accounts_you've_favorited.json"]["structure"]["relationships_feed_favorites"]:
            if "string_list_data" in item and len(item["string_list_data"]) > 0:
                for item2 in item["string_list_data"]:
                    if "timestamp" in item2:
                        account = item["title"]
                        views = item2["timestamp"]
                        if account in account_views:
                            account_views[account] += views
                        else:
                            account_views[account] = views
    if "followers_1.json" in data and "string_list_data" in data["followers_1.json"]["structure"]:
        for item in data["followers_1.json"]["structure"]["string_list_data"]:
            if "timestamp" in item:
                account = "Followers"
                views = item["timestamp"]
                if account in account_views:
                    account_views[account] += views
                else:
                    account_views[account] = views
    if "following.json" in data and "string_list_data" in data["following.json"]["structure"]:
        for item in data["following.json"]["structure"]["string_list_data"]:
            if "timestamp" in item:
                account = "Following"
                views = item["timestamp"]
                if account in account_views:
                    account_views[account] += views
                else:
                    account_views[account] = views

# Function to write data to CSV file
def write_to_csv(data):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Account', 'Post Views', 'Video Views']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, views in data.items():
            writer.writerow({'Account': account, 'Post Views': 0, 'Video Views': 0})

# Main function
def main():
    try:
        # Walk through the directory structure
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Check if the file is a JSON file
                if file.endswith(".json"):
                    data = parse_json(file_path)
                    if data is not None:
                        extract_data(data)
        # Write data to CSV file
        write_to_csv(account_views)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()