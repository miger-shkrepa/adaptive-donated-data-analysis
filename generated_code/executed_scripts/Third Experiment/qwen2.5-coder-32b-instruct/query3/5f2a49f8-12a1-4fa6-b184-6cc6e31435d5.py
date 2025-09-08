import os
import csv
from datetime import datetime, timedelta

root_dir = "root_dir"

def get_posts_viewed_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = eval(file.read())
            return data['impressions_history_posts_seen']
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while reading the posts_viewed.json file - {str(e)}")

def convert_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')

def aggregate_posts_viewed(posts_viewed_data):
    daily_counts = {}
    for post in posts_viewed_data:
        date = convert_timestamp_to_date(post['string_map_data']['Time']['timestamp'])
        if date in daily_counts:
            daily_counts[date] += 1
        else:
            daily_counts[date] = 1
    return daily_counts

def calculate_weekly_counts(daily_counts):
    weekly_counts = {}
    for date_str, count in daily_counts.items():
        date = datetime.strptime(date_str, '%Y-%m-%d')
        year, week_number, _ = date.isocalendar()
        week_key = f"Week {year}-{week_number:02}"
        if week_key in weekly_counts:
            weekly_counts[week_key] += count
        else:
            weekly_counts[week_key] = count
    return weekly_counts

def write_to_csv(daily_counts, weekly_counts, output_path):
    try:
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            for date, count in daily_counts.items():
                writer.writerow([date, count, 'Daily'])
            for week, count in weekly_counts.items():
                writer.writerow([week, count, 'Weekly'])
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while writing to the CSV file - {str(e)}")

def main():
    posts_viewed_file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(posts_viewed_file_path):
        write_to_csv({}, {}, 'query_responses/results.csv')
        return
    
    posts_viewed_data = get_posts_viewed_data(posts_viewed_file_path)
    daily_counts = aggregate_posts_viewed(posts_viewed_data)
    weekly_counts = calculate_weekly_counts(daily_counts)
    
    write_to_csv(daily_counts, weekly_counts, 'query_responses/results.csv')

if __name__ == "__main__":
    main()