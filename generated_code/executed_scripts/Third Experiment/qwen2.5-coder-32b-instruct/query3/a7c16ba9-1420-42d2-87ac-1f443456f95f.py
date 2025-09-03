import os
import csv
import json
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_week_number(date):
    return date.isocalendar()[1]

def process_posts_viewed(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        posts_viewed = data.get('impressions_history_posts_seen', [])
        return posts_viewed

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        posts_viewed_file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(posts_viewed_file_path):
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
        
        posts_viewed_data = process_posts_viewed(posts_viewed_file_path)
        
        daily_counts = {}
        weekly_counts = {}
        
        for post in posts_viewed_data:
            timestamp = post['string_map_data']['Time']['timestamp']
            date = datetime.fromtimestamp(timestamp)
            date_str = date.strftime('%Y-%m-%d')
            week_str = f"Week {date.year}-{get_week_number(date):02d}"
            
            if date_str in daily_counts:
                daily_counts[date_str] += 1
            else:
                daily_counts[date_str] = 1
            
            if week_str in weekly_counts:
                weekly_counts[week_str] += 1
            else:
                weekly_counts[week_str] = 1
        
        results = []
        for date, count in daily_counts.items():
            results.append([date, count, 'Daily'])
        
        for week, count in weekly_counts.items():
            results.append([week, count, 'Weekly'])
        
        results.sort(key=lambda x: (x[0], x[2]))
        
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            writer.writerows(results)
    
    except FileNotFoundError as e:
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
        print(e)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()