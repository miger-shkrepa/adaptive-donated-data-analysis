import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The specified JSON file is not properly formatted.")

def get_posts_viewed_data(root_dir):
    posts_viewed_data = []
    try:
        ads_and_topics_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics')
        posts_viewed_file = os.path.join(ads_and_topics_path, 'posts_viewed.json')

        if not os.path.exists(posts_viewed_file):
            return []

        data = load_json_file(posts_viewed_file)
        impressions_history = data.get('impressions_history_posts_seen', [])

        for entry in impressions_history:
            string_map_data = entry.get('string_map_data', {})
            timestamp = string_map_data.get('Time', {}).get('timestamp')
            if timestamp:
                date = datetime.fromtimestamp(timestamp)
                posts_viewed_data.append(date)

    except Exception as e:
        print(f"Error processing posts_viewed.json: {e}")

    return posts_viewed_data

def aggregate_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}

    for date in posts_viewed_data:
        date_str = date.strftime('%Y-%m-%d')
        week_str = f"Week {date.strftime('%Y-%W')}"

        daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1

    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    posts_viewed_data = get_posts_viewed_data(root_dir)
    daily_counts, weekly_counts = aggregate_data(posts_viewed_data)
    write_to_csv(daily_counts, weekly_counts)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")