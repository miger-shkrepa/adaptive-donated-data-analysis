import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    try:
        posts_viewed_daily = {}
        posts_viewed_weekly = {}

        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate over all files in the directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == "posts_viewed.json":
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        # Try to parse the JSON file
                        try:
                            import json
                            data = json.load(file)
                            for post in data['impressions_history_posts_seen']:
                                time = post['string_map_data']['Time']['timestamp']
                                date = datetime.fromtimestamp(time)
                                date_str = date.strftime('%Y-%m-%d')
                                week_str = date.strftime('Week %Y-%W')

                                # Update daily posts viewed
                                if date_str in posts_viewed_daily:
                                    posts_viewed_daily[date_str] += 1
                                else:
                                    posts_viewed_daily[date_str] = 1

                                # Update weekly posts viewed
                                if week_str in posts_viewed_weekly:
                                    posts_viewed_weekly[week_str] += 1
                                else:
                                    posts_viewed_weekly[week_str] = 1
                        except json.JSONDecodeError:
                            raise ValueError("Error: The JSON file is not well-formed.")

        return posts_viewed_daily, posts_viewed_weekly

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(posts_viewed_daily, posts_viewed_weekly):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

            # Write daily posts viewed
            for date, count in posts_viewed_daily.items():
                writer.writerow([date, count, "Daily"])

            # Write weekly posts viewed
            for week, count in posts_viewed_weekly.items():
                writer.writerow([week, count, "Weekly"])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        posts_viewed_daily, posts_viewed_weekly = get_posts_viewed(root_dir)
        write_to_csv(posts_viewed_daily, posts_viewed_weekly)
    except Exception as e:
        print(f"Error: {str(e)}")
        # If an error occurs, write only the column headers to the CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

if __name__ == "__main__":
    main()