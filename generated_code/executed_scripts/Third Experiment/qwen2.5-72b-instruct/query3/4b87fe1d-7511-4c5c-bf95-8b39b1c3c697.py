import os
import json
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_posts_viewed_data():
    try:
        ads_info_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if not os.path.exists(ads_info_path):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
        
        with open(ads_info_path, 'r') as file:
            data = json.load(file)
        
        posts_viewed = []
        for item in data.get("impressions_history_posts_seen", []):
            timestamp = item["string_map_data"]["Time"]["timestamp"]
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            posts_viewed.append((date, 1))
        
        return posts_viewed
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def aggregate_data(posts_viewed):
    daily_counts = {}
    weekly_counts = {}
    
    for date, count in posts_viewed:
        if date not in daily_counts:
            daily_counts[date] = 0
        daily_counts[date] += count
        
        week = "Week " + datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%W')
        if week not in weekly_counts:
            weekly_counts[week] = 0
        weekly_counts[week] += count
    
    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for date, count in daily_counts.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
            
            for week, count in weekly_counts.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        posts_viewed = get_posts_viewed_data()
        daily_counts, weekly_counts = aggregate_data(posts_viewed)
        write_to_csv(daily_counts, weekly_counts)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()