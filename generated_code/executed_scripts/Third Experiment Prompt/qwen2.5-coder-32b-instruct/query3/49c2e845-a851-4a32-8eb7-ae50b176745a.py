import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_posts_viewed_data(root_dir):
    posts_viewed_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(posts_viewed_file_path):
        return []
    
    try:
        with open(posts_viewed_file_path, 'r', encoding='utf-8') as file:
            data = eval(file.read())
    except Exception as e:
        raise ValueError(f"ValueError: Failed to read or parse the posts_viewed.json file. {str(e)}")
    
    posts_viewed_data = []
    for entry in data.get("impressions_history_posts_seen", []):
        timestamp = entry.get("string_map_data", {}).get("Time", {}).get("timestamp", None)
        if timestamp:
            date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
            posts_viewed_data.append(date)
    
    return posts_viewed_data

def aggregate_posts_viewed_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}
    
    for date in posts_viewed_data:
        datetime_obj = datetime.strptime(date, '%Y-%m-%d')
        daily_key = date
        weekly_key = f"Week {datetime_obj.strftime('%Y-%W')}"
        
        if daily_key not in daily_counts:
            daily_counts[daily_key] = 0
        daily_counts[daily_key] += 1
        
        if weekly_key not in weekly_counts:
            weekly_counts[weekly_key] = 0
        weekly_counts[weekly_key] += 1
    
    aggregated_data = []
    for date, count in daily_counts.items():
        aggregated_data.append((date, count, 'Daily'))
    
    for week, count in weekly_counts.items():
        aggregated_data.append((week, count, 'Weekly'))
    
    return aggregated_data

def write_to_csv(aggregated_data):
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date/Week', 'Posts Viewed', 'Type'])
        csvwriter.writerows(aggregated_data)

def main():
    try:
        posts_viewed_data = get_posts_viewed_data(root_dir)
        aggregated_data = aggregate_posts_viewed_data(posts_viewed_data)
        write_to_csv(aggregated_data)
    except Exception as e:
        write_to_csv([])  # Write only headers if there's an error
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()