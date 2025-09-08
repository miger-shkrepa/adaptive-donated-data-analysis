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
        print(f"Warning: The file {posts_viewed_file_path} does not exist. Returning an empty CSV.")
        return []

    try:
        with open(posts_viewed_file_path, 'r') as file:
            data = eval(file.read())
    except Exception as e:
        raise ValueError(f"ValueError: Failed to read or parse the file {posts_viewed_file_path}. Reason: {str(e)}")

    posts_viewed_data = []
    for entry in data.get("impressions_history_posts_seen", []):
        string_map_data = entry.get("string_map_data", {})
        timestamp = string_map_data.get("Time", {}).get("timestamp", None)
        if timestamp:
            date = datetime.fromtimestamp(timestamp / 1000)  # Convert milliseconds to seconds
            posts_viewed_data.append(date)

    return posts_viewed_data

def aggregate_posts_viewed_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}

    for date in posts_viewed_data:
        date_str = date.strftime('%Y-%m-%d')
        week_str = date.strftime('Week %Y-%W')

        if date_str in daily_counts:
            daily_counts[date_str] += 1
        else:
            daily_counts[date_str] = 1

        if week_str in weekly_counts:
            weekly_counts[week_str] += 1
        else:
            weekly_counts[week_str] = 1

    aggregated_data = []

    for date_str, count in daily_counts.items():
        aggregated_data.append((date_str, count, 'Daily'))

    for week_str, count in weekly_counts.items():
        aggregated_data.append((week_str, count, 'Weekly'))

    return aggregated_data

def write_to_csv(aggregated_data):
    output_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date/Week', 'Posts Viewed', 'Type'])
        csvwriter.writerows(aggregated_data)

def main():
    try:
        posts_viewed_data = get_posts_viewed_data(root_dir)
        aggregated_data = aggregate_posts_viewed_data(posts_viewed_data)
        write_to_csv(aggregated_data)
    except Exception as e:
        print(f"Error: {str(e)}")
        write_to_csv([])  # Write an empty CSV with headers if there's an error

if __name__ == "__main__":
    main()