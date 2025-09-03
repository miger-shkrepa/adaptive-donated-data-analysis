import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

def get_daily_and_weekly_counts(data, key, timestamp_key):
    daily_counts = {}
    weekly_counts = {}
    for item in data.get(key, []):
        for string_data in item.get('string_list_data', []):
            timestamp = string_data.get(timestamp_key)
            if timestamp:
                date = datetime.fromtimestamp(timestamp)
                date_str = date.strftime('%Y-%m-%d')
                week_str = f"Week {date.strftime('%Y-%W')}"
                daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
                weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1
    return daily_counts, weekly_counts

def write_csv(daily_counts, weekly_counts):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
        
        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        liked_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
        saved_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'saved', 'saved_posts.json')
        
        liked_posts_data = {}
        saved_posts_data = {}
        
        if os.path.exists(liked_posts_path):
            liked_posts_data = load_json_file(liked_posts_path)
        
        if os.path.exists(saved_posts_path):
            saved_posts_data = load_json_file(saved_posts_path)
        
        liked_daily, liked_weekly = get_daily_and_weekly_counts(liked_posts_data, 'likes_media_likes', 'timestamp')
        saved_daily, saved_weekly = get_daily_and_weekly_counts(saved_posts_data, 'saved_saved_media', 'timestamp')
        
        daily_counts = {**liked_daily, **saved_daily}
        weekly_counts = {**liked_weekly, **saved_weekly}
        
        write_csv(daily_counts, weekly_counts)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()