import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize variables to store posts viewed
        daily_posts_viewed = {}
        weekly_posts_viewed = {}

        # Iterate over all files in the directory
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                # Check if file is 'posts_viewed.json'
                if file == 'posts_viewed.json':
                    file_path = os.path.join(root, file)
                    try:
                        # Open and read the file
                        with open(file_path, 'r') as f:
                            # Since the structure of 'posts_viewed.json' is not provided, 
                            # we assume it contains a list of posts with their view timestamps
                            import json
                            data = json.load(f)
                            for post in data['impressions_history_posts_seen']:
                                timestamp = post['string_map_data']['Time']['timestamp']
                                date = datetime.fromtimestamp(timestamp)
                                date_str = date.strftime('%Y-%m-%d')
                                week_str = 'Week ' + date.strftime('%Y-%W')
                                if date_str not in daily_posts_viewed:
                                    daily_posts_viewed[date_str] = 0
                                daily_posts_viewed[date_str] += 1
                                if week_str not in weekly_posts_viewed:
                                    weekly_posts_viewed[week_str] = 0
                                weekly_posts_viewed[week_str] += 1
                    except Exception as e:
                        print(f"Error reading {file_path}: {str(e)}")

        return daily_posts_viewed, weekly_posts_viewed

    except Exception as e:
        raise ValueError("ValueError: " + str(e))

def write_to_csv(daily_posts_viewed, weekly_posts_viewed):
    try:
        # Create the 'query_responses' directory if it does not exist
        if not os.path.exists('query_responses'):
            os.makedirs('query_responses')

        # Write to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for date, count in daily_posts_viewed.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': count, 'Type': 'Daily'})
            for week, count in weekly_posts_viewed.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': count, 'Type': 'Weekly'})

    except Exception as e:
        raise ValueError("ValueError: " + str(e))

def main():
    try:
        daily_posts_viewed, weekly_posts_viewed = get_posts_viewed(root_dir)
        write_to_csv(daily_posts_viewed, weekly_posts_viewed)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except ValueError as e:
        raise ValueError("ValueError: " + str(e))
    except Exception as e:
        raise ValueError("ValueError: " + str(e))

if __name__ == "__main__":
    main()