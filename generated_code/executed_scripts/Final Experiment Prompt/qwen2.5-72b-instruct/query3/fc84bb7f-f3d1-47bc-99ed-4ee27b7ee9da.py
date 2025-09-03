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

def get_weekly_date(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('Week %Y-%W')

def get_daily_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def process_data(data):
    daily_counts = {}
    weekly_counts = {}

    for entry in data.get("impressions_history_posts_seen", []):
        timestamp = entry.get("string_map_data", {}).get("Time", {}).get("timestamp")
        if timestamp is not None:
            daily_date = get_daily_date(timestamp)
            weekly_date = get_weekly_date(timestamp)

            daily_counts[daily_date] = daily_counts.get(daily_date, 0) + 1
            weekly_counts[weekly_date] = weekly_counts.get(weekly_date, 0) + 1

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
            raise FileNotFoundError("Error: The root directory does not exist.")

        file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(file_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        data = load_json_data(file_path)
        daily_counts, weekly_counts = process_data(data)
        write_csv(daily_counts, weekly_counts)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()