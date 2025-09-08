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

def get_week_number(date):
    return date.strftime("Week %Y-%W")

def process_posts_viewed(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}
    for entry in posts_viewed_data:
        timestamp = entry['string_map_data']['Time']['timestamp']
        date = datetime.fromtimestamp(timestamp)
        date_str = date.strftime('%Y-%m-%d')
        week_str = get_week_number(date)
        
        daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1

    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts):
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
        
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(posts_viewed_path):
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        posts_viewed_data = load_json_data(posts_viewed_path)
        daily_counts, weekly_counts = process_posts_viewed(posts_viewed_data['impressions_history_posts_seen'])
        write_to_csv(daily_counts, weekly_counts)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()