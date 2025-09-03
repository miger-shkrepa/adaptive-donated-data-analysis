import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def parse_timestamp(timestamp):
    try:
        return datetime.fromtimestamp(timestamp)
    except ValueError as e:
        raise ValueError(f"Error: Invalid timestamp value - {e}")

def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError("Error: FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSONDecodeError: {e}")

def generate_csv(data):
    daily_counts = {}
    weekly_counts = {}

    for entry in data.get("impressions_history_posts_seen", []):
        string_map_data = entry.get("string_map_data", {})
        timestamp = string_map_data.get("Time", {}).get("timestamp")

        if timestamp is None:
            continue

        dt = parse_timestamp(timestamp)
        date_str = dt.strftime('%Y-%m-%d')
        week_str = f"Week {dt.strftime('%Y-%W')}"

        daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1

    return daily_counts, weekly_counts

def write_csv(daily_counts, weekly_counts):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

def main():
    file_path = os.path.join(root_dir, 'ads_information/ads_and_topics/posts_viewed.json')

    try:
        data = process_json_file(file_path)
        daily_counts, weekly_counts = generate_csv(data)
        write_csv(daily_counts, weekly_counts)
    except FileNotFoundError as e:
        print(e)
        write_csv({}, {})
    except ValueError as e:
        print(e)
        write_csv({}, {})

if __name__ == "__main__":
    main()