import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_post_views(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize variables to store post views
        daily_views = {}
        weekly_views = {}

        # Iterate over the files in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                file_path = os.path.join(root_dir, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    # Check if the file contains post data
                    if 'media_metadata' in data:
                        for post in data['media_metadata']:
                            # Get the creation timestamp of the post
                            creation_timestamp = post.get('creation_timestamp')
                            if creation_timestamp:
                                # Convert the timestamp to a datetime object
                                date = datetime.fromtimestamp(creation_timestamp)
                                # Get the date and week of the post
                                date_str = date.strftime('%Y-%m-%d')
                                week_str = f"Week {date.strftime('%Y-%U')}"

                                # Increment the daily and weekly view counts
                                daily_views[date_str] = daily_views.get(date_str, 0) + 1
                                weekly_views[week_str] = weekly_views.get(week_str, 0) + 1

        return daily_views, weekly_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(daily_views, weekly_views):
    try:
        # Create the results directory if it does not exist
        results_dir = 'query_responses'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Save the results to a CSV file
        with open(os.path.join(results_dir, 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            for date, views in daily_views.items():
                writer.writerow([date, views, 'Daily'])
            for week, views in weekly_views.items():
                writer.writerow([week, views, 'Weekly'])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        daily_views, weekly_views = get_post_views(root_dir)
        save_to_csv(daily_views, weekly_views)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()