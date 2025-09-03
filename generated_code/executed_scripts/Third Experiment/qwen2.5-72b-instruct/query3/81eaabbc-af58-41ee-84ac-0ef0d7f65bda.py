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
        
        # Check if the necessary files exist
        posts_viewed_file = os.path.join(root_dir, "your_instagram_activity", "content", "profile_photos.json")
        if not os.path.exists(posts_viewed_file):
            return posts_viewed  # Return empty list if the file is not found
        
        with open(posts_viewed_file, 'r') as file:
            data = json.load(file)
            for item in data.get("ig_profile_picture", []):
                timestamp = item.get("creation_timestamp")
                if timestamp:
                    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    posts_viewed.append((date, 1))
    
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")
    
    return posts_viewed

def aggregate_data(posts_viewed):
    daily_data = {}
    weekly_data = {}
    
    for date, count in posts_viewed:
        if date not in daily_data:
            daily_data[date] = 0
        daily_data[date] += count
        
        week = datetime.strptime(date, '%Y-%m-%d').strftime('Week %Y-%W')
        if week not in weekly_data:
            weekly_data[week] = 0
        weekly_data[week] += count
    
    return daily_data, weekly_data

def write_to_csv(daily_data, weekly_data):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for date, count in daily_data.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
        
        for week, count in weekly_data.items():
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
        
        daily_data, weekly_data = aggregate_data(posts_viewed)
        write_to_csv(daily_data, weekly_data)
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()