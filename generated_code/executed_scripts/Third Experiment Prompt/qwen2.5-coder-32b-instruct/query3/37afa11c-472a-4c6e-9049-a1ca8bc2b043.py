import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_posts_viewed_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = eval(file.read())
            posts_viewed = data.get('impressions_history_posts_seen', [])
            return posts_viewed
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading posts_viewed.json file - {str(e)}")

def process_posts_viewed(posts_viewed):
    daily_counts = {}
    weekly_counts = {}

    for post in posts_viewed:
        timestamp = post['string_map_data']['Time']['timestamp']
        date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        week = datetime.fromtimestamp(timestamp).strftime('%Y-%W')

        if date in daily_counts:
            daily_counts[date] += 1
        else:
            daily_counts[date] = 1

        if week in weekly_counts:
            weekly_counts[week] += 1
        else:
            weekly_counts[week] = 1

    return daily_counts, weekly_counts

def write_to_csv(daily_counts, weekly_counts):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
        posts_viewed_file_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if not os.path.exists(posts_viewed_file_path):
            write_to_csv({}, {})
            return

        posts_viewed = get_posts_viewed_data(posts_viewed_file_path)
        daily_counts, weekly_counts = process_posts_viewed(posts_viewed)
        write_to_csv(daily_counts, weekly_counts)

    except FileNotFoundError as fnf_error:
        print(fnf_error)
        write_to_csv({}, {})
    except ValueError as ve_error:
        print(ve_error)
        write_to_csv({}, {})

if __name__ == "__main__":
    main()