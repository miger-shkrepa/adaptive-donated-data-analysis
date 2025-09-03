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

        # Iterate over all files in the root directory
        for filename in os.listdir(root_dir):
            file_path = os.path.join(root_dir, filename)

            # Check if the file is a JSON file
            if filename.endswith(".json"):
                try:
                    # Open and load the JSON file
                    with open(file_path, 'r') as file:
                        data = json.load(file)

                    # Check if the JSON file contains post data
                    if 'creation_timestamp' in data:
                        # Convert the creation timestamp to a datetime object
                        timestamp = datetime.fromtimestamp(data['creation_timestamp'])

                        # Get the date and week of the post
                        date = timestamp.strftime('%Y-%m-%d')
                        week = timestamp.strftime('Week %Y-%U')

                        # Increment the daily and weekly view counts
                        daily_views[date] = daily_views.get(date, 0) + 1
                        weekly_views[week] = weekly_views.get(week, 0) + 1

                except json.JSONDecodeError:
                    raise ValueError("ValueError: Invalid JSON file.")

            # Check if the file is a directory
            elif os.path.isdir(file_path):
                # Recursively call the function on the subdirectory
                get_post_views(file_path)

        return daily_views, weekly_views

    except Exception as e:
        raise ValueError("ValueError: " + str(e))

def save_to_csv(daily_views, weekly_views):
    try:
        # Create the output CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

            # Write the daily views
            for date, views in daily_views.items():
                writer.writerow([date, views, "Daily"])

            # Write the weekly views
            for week, views in weekly_views.items():
                writer.writerow([week, views, "Weekly"])

    except Exception as e:
        raise ValueError("ValueError: " + str(e))

def main():
    try:
        daily_views, weekly_views = get_post_views(root_dir)
        save_to_csv(daily_views, weekly_views)

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except ValueError as e:
        raise ValueError("ValueError: " + str(e))

if __name__ == "__main__":
    main()