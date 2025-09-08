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
        raise FileNotFoundError("Error: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

def get_posts_viewed_data():
    posts_viewed_data = []
    try:
        posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        data = load_json_data(posts_viewed_file)
        for item in data.get("impressions_history_posts_seen", []):
            timestamp = item["string_map_data"]["Time"]["timestamp"]
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            posts_viewed_data.append((date, 1))
    except FileNotFoundError:
        print("Warning: posts_viewed.json not found, treating its contribution as 0.")
    return posts_viewed_data

def aggregate_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}
    for date, count in posts_viewed_data:
        if date not in daily_counts:
            daily_counts[date] = 0
        daily_counts[date] += count

        week = "Week " + datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%W')
        if week not in weekly_counts:
            weekly_counts[week] = 0
        weekly_counts[week] += count

    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
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

    posts_viewed_data = get_posts_viewed_data()
    if not posts_viewed_data:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        return

    daily_counts, weekly_counts = aggregate_data(posts_viewed_data)
    write_to_csv(daily_counts, weekly_counts)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)