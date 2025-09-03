import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def get_posts_viewed_data(posts_viewed_file):
    try:
        data = load_json_data(posts_viewed_file)
        posts_viewed = data.get("impressions_history_posts_seen", [])
        return posts_viewed
    except Exception as e:
        raise ValueError(f"Error: Failed to process posts_viewed data - {str(e)}")

def aggregate_daily_weekly(posts_viewed):
    daily_counts = {}
    weekly_counts = {}
    for entry in posts_viewed:
        timestamp = entry.get("string_map_data", {}).get("Time", {}).get("timestamp")
        if timestamp:
            date = datetime.fromtimestamp(timestamp)
            date_str = date.strftime('%Y-%m-%d')
            week_str = f"Week {date.strftime('%Y-%W')}"
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
            weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1
    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for date, count in daily_counts.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
            for week, count in weekly_counts.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV - {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")
        
        posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return
        
        posts_viewed = get_posts_viewed_data(posts_viewed_file)
        daily_counts, weekly_counts = aggregate_daily_weekly(posts_viewed)
        write_to_csv(daily_counts, weekly_counts)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()