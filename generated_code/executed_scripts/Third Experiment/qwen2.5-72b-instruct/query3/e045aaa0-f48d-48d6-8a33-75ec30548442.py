import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_posts_viewed_data():
    posts_viewed = []
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        posts_path = os.path.join(root_dir, "posts", "your_posts.json")
        if not os.path.exists(posts_path):
            return posts_viewed  # Return empty list if the file does not exist
        
        with open(posts_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            posts = data.get("posts", [])
            for post in posts:
                timestamp = post.get("timestamp", None)
                if timestamp is None:
                    continue
                date = datetime.fromtimestamp(timestamp)
                posts_viewed.append(date)
    except json.JSONDecodeError:
        raise ValueError("Error: JSON data is not properly formatted.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")
    
    return posts_viewed

def aggregate_data(posts_viewed):
    daily_counts = {}
    weekly_counts = {}
    for date in posts_viewed:
        date_str = date.strftime('%Y-%m-%d')
        week_str = f"Week {date.strftime('%Y-%W')}"
        daily_counts[date_str] = daily_counts.get(date_str, 0) + 1
        weekly_counts[week_str] = weekly_counts.get(week_str, 0) + 1
    
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
    try:
        posts_viewed = get_posts_viewed_data()
        if not posts_viewed:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return
        
        daily_counts, weekly_counts = aggregate_data(posts_viewed)
        write_to_csv(daily_counts, weekly_counts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()