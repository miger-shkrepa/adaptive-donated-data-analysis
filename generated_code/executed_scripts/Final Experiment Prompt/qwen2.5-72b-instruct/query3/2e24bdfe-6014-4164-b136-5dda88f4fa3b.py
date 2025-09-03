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

def get_daily_and_weekly_counts(posts_seen):
    daily_counts = {}
    weekly_counts = {}

    for post in posts_seen:
        timestamp = post.get("string_map_data", {}).get("Time", {}).get("timestamp")
        if timestamp is None:
            continue

        try:
            date = datetime.fromtimestamp(timestamp)
            date_str = date.strftime('%Y-%m-%d')
            week_str = "Week " + date.strftime('%Y-%W')

            if date_str in daily_counts:
                daily_counts[date_str] += 1
            else:
                daily_counts[date_str] = 1

            if week_str in weekly_counts:
                weekly_counts[week_str] += 1
            else:
                weekly_counts[week_str] = 1
        except (ValueError, OSError):
            continue

    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
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

        file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if not os.path.exists(file_path):
            write_to_csv({}, {}, 'query_responses/results.csv')
            return

        data = load_json_data(file_path)
        posts_seen = data.get("impressions_history_posts_seen", [])
        daily_counts, weekly_counts = get_daily_and_weekly_counts(posts_seen)
        write_to_csv(daily_counts, weekly_counts, 'query_responses/results.csv')

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()