import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to load JSON data from a file
def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: Failed to decode JSON from {file_path}.")

# Function to get daily and weekly post views
def get_post_views(root_dir):
    daily_views = {}
    weekly_views = {}

    ads_and_topics_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    
    if not os.path.exists(ads_and_topics_path):
        return daily_views, weekly_views

    try:
        data = load_json_data(ads_and_topics_path)
        posts_viewed = data.get('impressions_history_posts_seen', [])
        
        for entry in posts_viewed:
            string_map_data = entry.get('string_map_data', {})
            time_data = string_map_data.get('Time', {})
            timestamp = time_data.get('timestamp')
            
            if timestamp:
                date = datetime.fromtimestamp(timestamp)
                date_str = date.strftime('%Y-%m-%d')
                week_str = f"Week {date.strftime('%Y-%W')}"
                
                daily_views[date_str] = daily_views.get(date_str, 0) + 1
                weekly_views[week_str] = weekly_views.get(week_str, 0) + 1
    except Exception as e:
        print(f"Error processing {ads_and_topics_path}: {e}")

    return daily_views, weekly_views

# Function to write the results to a CSV file
def write_to_csv(daily_views, weekly_views):
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for date, count in daily_views.items():
            writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
        
        for week, count in weekly_views.items():
            writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        daily_views, weekly_views = get_post_views(root_dir)
        write_to_csv(daily_views, weekly_views)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()