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
    try:
        for entry in data['impressions_history_posts_seen']:
            timestamp = entry['string_map_data']['Time']['timestamp']
            date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
            posts_viewed_data.append((date, 'Daily'))
    except KeyError as e:
        raise ValueError(f"ValueError: The file {posts_viewed_file_path} does not have the expected structure. Missing key: {str(e)}")

    return posts_viewed_data

def aggregate_data(posts_viewed_data):
    daily_counts = {}
    weekly_counts = {}

    for date, period in posts_viewed_data:
        if period == 'Daily':
            if date not in daily_counts:
                daily_counts[date] = 0
            daily_counts[date] += 1

            week = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%W')
            if week not in weekly_counts:
                weekly_counts[week] = 0
            weekly_counts[week] += 1

    aggregated_data = []
    for date, count in daily_counts.items():
        aggregated_data.append((date, count, 'Daily'))

    for week, count in weekly_counts.items():
        aggregated_data.append((f"Week {week}", count, 'Weekly'))

    return aggregated_data

def write_to_csv(aggregated_data):
    output_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date/Week', 'Posts Viewed', 'Type'])
        for row in aggregated_data:
            csvwriter.writerow(row)

def main():
    try:
        posts_viewed_data = get_posts_viewed_data(root_dir)
        aggregated_data = aggregate_data(posts_viewed_data)
        write_to_csv(aggregated_data)
    except Exception as e:
        print(f"Error: {str(e)}")
        write_to_csv([])

if __name__ == "__main__":
    main()