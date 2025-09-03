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
        
        if date_str in daily_counts:
            daily_counts[date_str] += 1
        else:
            daily_counts[date_str] = 1
        
        if week_str in weekly_counts:
            weekly_counts[week_str] += 1
        else:
            weekly_counts[week_str] = 1

    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for date, count in daily_counts.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
            
            for week, count in weekly_counts.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})
    except IOError:
        raise IOError("Error: Unable to write to the CSV file.")

def main():
    try:
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        posts_viewed_data = load_json_data(posts_viewed_path)
        daily_counts, weekly_counts = process_posts_viewed(posts_viewed_data['impressions_history_posts_seen'])
        write_to_csv(daily_counts, weekly_counts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()