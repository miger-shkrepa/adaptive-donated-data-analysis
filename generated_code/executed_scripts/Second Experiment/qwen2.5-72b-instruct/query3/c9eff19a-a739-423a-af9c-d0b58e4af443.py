import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def get_posts_viewed_data():
    posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if not os.path.exists(posts_viewed_file):
        return []
    data = load_json(posts_viewed_file)
    posts_viewed = data.get("impressions_history_posts_seen", [])
    return posts_viewed

def aggregate_daily_weekly(posts_viewed):
    daily_counts = {}
    weekly_counts = {}
    for post in posts_viewed:
        timestamp = post["string_map_data"]["Time"]["timestamp"]
        date = datetime.fromtimestamp(timestamp).date()
        week = date.strftime("Week %Y-%W")
        daily_counts[date] = daily_counts.get(date, 0) + 1
        weekly_counts[week] = weekly_counts.get(week, 0) + 1

    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for date, count in daily_counts.items():
                writer.writerow({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': count, 'Type': 'Daily'})

            for week, count in weekly_counts.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV file. Reason: {str(e)}")

def main():
    try:
        posts_viewed = get_posts_viewed_data()
        daily_counts, weekly_counts = aggregate_daily_weekly(posts_viewed)
        write_to_csv(daily_counts, weekly_counts)
    except FileNotFoundError as e:
        print(e)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()