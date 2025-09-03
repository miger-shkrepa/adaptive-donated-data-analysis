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

        # Initialize dictionaries to store daily and weekly post views
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
                        week = f"Week {timestamp.strftime('%Y-%U')}"

                        # Increment the daily and weekly post views
                        daily_views[date] = daily_views.get(date, 0) + 1
                        weekly_views[week] = weekly_views.get(week, 0) + 1

                except json.JSONDecodeError:
                    raise ValueError("ValueError: The JSON file is malformed.")

        return daily_views, weekly_views

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

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

            # Write daily post views
            for date, views in daily_views.items():
                writer.writerow([date, views, 'Daily'])

            # Write weekly post views
            for week, views in weekly_views.items():
                writer.writerow([week, views, 'Weekly'])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        daily_views, weekly_views = get_post_views(root_dir)
        save_to_csv(daily_views, weekly_views)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {str(e)}")
    except ValueError as e:
        raise ValueError(f"ValueError: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

if __name__ == "__main__":
    main()