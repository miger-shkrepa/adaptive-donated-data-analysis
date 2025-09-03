import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_posts_viewed_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = eval(file.read())
            posts_viewed = data.get('impressions_history_posts_seen', [])
            return posts_viewed
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The required file does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")

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
        raise ValueError(f"ValueError: Error writing to CSV file {output_path}: {str(e)}")

def main():
    try:
        # Define the path to the posts_viewed.json file
        posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

        # Check if the file exists
        if not os.path.exists(posts_viewed_path):
            # If the file does not exist, create an empty CSV with headers
            write_to_csv({}, {}, 'query_responses/results.csv')
            return

        # Get the posts viewed data
        posts_viewed = get_posts_viewed_data(posts_viewed_path)

        # Process the posts viewed data to get daily and weekly counts
        daily_counts, weekly_counts = process_posts_viewed(posts_viewed)

        # Write the results to a CSV file
        write_to_csv(daily_counts, weekly_counts, 'query_responses/results.csv')

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()