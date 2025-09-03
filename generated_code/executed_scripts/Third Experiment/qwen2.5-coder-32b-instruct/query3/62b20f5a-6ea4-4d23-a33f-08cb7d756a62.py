import os
import csv
from datetime import datetime, timedelta

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

def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp)
    except (OSError, OverflowError, ValueError):
        raise ValueError(f"ValueError: Invalid timestamp value {timestamp}.")

def aggregate_posts(data, daily_posts, weekly_posts):
    for item in data:
        timestamp = parse_timestamp(item['string_list_data'][0]['timestamp'])
        date_str = timestamp.strftime('%Y-%m-%d')
        week_str = f"Week {timestamp.strftime('%Y-%W')}"

        if date_str in daily_posts:
            daily_posts[date_str] += 1
        else:
            daily_posts[date_str] = 1

        if week_str in weekly_posts:
            weekly_posts[week_str] += 1
        else:
            weekly_posts[week_str] = 1

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        likes_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
        saved_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

        daily_posts = {}
        weekly_posts = {}

        if os.path.exists(likes_path):
            likes_data = get_json_data(likes_path)
            aggregate_posts(likes_data['likes_media_likes'], daily_posts, weekly_posts)

        if os.path.exists(saved_path):
            saved_data = get_json_data(saved_path)
            aggregate_posts(saved_data['saved_saved_media'], daily_posts, weekly_posts)

        output_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

            for date, count in daily_posts.items():
                writer.writerow([date, count, "Daily"])

            for week, count in weekly_posts.items():
                writer.writerow([week, count, "Weekly"])

    except Exception as e:
        output_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()