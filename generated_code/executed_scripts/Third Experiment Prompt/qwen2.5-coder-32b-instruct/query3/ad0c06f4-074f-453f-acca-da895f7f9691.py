import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_posts_viewed_data(root_dir):
    posts_viewed_data = []
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(posts_viewed_path):
        return posts_viewed_data
    
    try:
        with open(posts_viewed_path, 'r', encoding='utf-8') as file:
            data = eval(file.read())
            for entry in data.get("impressions_history_posts_seen", []):
                timestamp = entry.get("string_map_data", {}).get("Time", {}).get("timestamp")
                if timestamp:
                    date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
                    posts_viewed_data.append((date, 1))
    except Exception as e:
        raise ValueError(f"ValueError: Error reading or parsing posts_viewed.json - {str(e)}")
    
    return posts_viewed_data

def aggregate_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}
    
    for date, count in posts_viewed_data:
        if date not in daily_counts:
            daily_counts[date] = 0
        daily_counts[date] += count
        
        year, week, _ = date.split('-')
        week_key = f"Week {year}-{week}"
        if week_key not in weekly_counts:
            weekly_counts[week_key] = 0
        weekly_counts[week_key] += count
    
    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            
            for date, count in daily_counts.items():
                writer.writerow([date, count, "Daily"])
            
            for week, count in weekly_counts.items():
                writer.writerow([week, count, "Weekly"])
    except Exception as e:
        raise ValueError(f"ValueError: Error writing to CSV file - {str(e)}")

def main():
    try:
        posts_viewed_data = get_posts_viewed_data(root_dir)
        daily_counts, weekly_counts = aggregate_data(posts_viewed_data)
        write_to_csv(daily_counts, weekly_counts, 'query_responses/results.csv')
    except Exception as e:
        print(e)
        # Create an empty CSV file with headers if an error occurs
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

if __name__ == "__main__":
    main()