import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def parse_liked_posts(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('likes_media_likes', [])
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def parse_saved_posts(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data.get('saved_saved_media', [])
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

def aggregate_data(liked_posts, saved_posts):
    daily_counts = {}
    weekly_counts = {}

    for post in liked_posts + saved_posts:
        timestamp = post.get('timestamp', 0)
        date = datetime.fromtimestamp(timestamp).date()
        week = date.isocalendar()[:2]
        week_str = f"Week {week[0]}-{week[1]:02d}"

        if date not in daily_counts:
            daily_counts[date] = 0
        daily_counts[date] += 1

        if week_str not in weekly_counts:
            weekly_counts[week_str] = 0
        weekly_counts[week_str] += 1

    return daily_counts, weekly_counts

def write_csv(daily_counts, weekly_counts):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_counts.items():
            writer.writerow({'Date/Week': date.strftime('%Y-%m-%d'), 'Posts Viewed': count, 'Type': 'Daily'})

        for week, count in weekly_counts.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

def main():
    liked_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json')
    saved_posts_path = os.path.join(root_dir, 'your_instagram_activity', 'saved', 'saved_posts.json')

    try:
        liked_posts = parse_liked_posts(liked_posts_path)
        saved_posts = parse_saved_posts(saved_posts_path)

        daily_counts, weekly_counts = aggregate_data(liked_posts, saved_posts)

        write_csv(daily_counts, weekly_counts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()