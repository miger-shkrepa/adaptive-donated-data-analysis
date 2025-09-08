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
        with open(posts_viewed_path, 'r') as file:
            data = eval(file.read())
            for entry in data.get("impressions_history_posts_seen", []):
                string_map_data = entry.get("string_map_data", {})
                timestamp = string_map_data.get("Time", {}).get("timestamp")
                if timestamp:
                    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
                    posts_viewed_data.append((date, 1))
    except Exception as e:
        raise ValueError(f"ValueError: Error reading or parsing posts_viewed.json - {str(e)}")
    
    return posts_viewed_data

def aggregate_posts_viewed_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}
    
    for date, count in posts_viewed_data:
        # Daily aggregation
        if date in daily_counts:
            daily_counts[date] += count
        else:
            daily_counts[date] = count
        
        # Weekly aggregation
        week = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%W')
        if week in weekly_counts:
            weekly_counts[week] += count
        else:
            weekly_counts[week] = count
    
    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            
            for date, count in daily_counts.items():
                csvwriter.writerow([date, count, 'Daily'])
            
            for week, count in weekly_counts.items():
                csvwriter.writerow([f"Week {week}", count, 'Weekly'])
    except Exception as e:
        raise ValueError(f"ValueError: Error writing to CSV file - {str(e)}")

def main():
    try:
        posts_viewed_data = get_posts_viewed_data(root_dir)
        daily_counts, weekly_counts = aggregate_posts_viewed_data(posts_viewed_data)
        write_to_csv(daily_counts, weekly_counts, 'query_responses/results.csv')
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    except ValueError as ve_error:
        print(ve_error)
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Date/Week', 'Posts Viewed', 'Type'])

if __name__ == "__main__":
    main()