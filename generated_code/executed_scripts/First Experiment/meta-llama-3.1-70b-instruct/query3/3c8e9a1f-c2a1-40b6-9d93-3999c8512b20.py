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
        daily_post_views = {}
        weekly_post_views = {}

        # Iterate over the files in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename), 'r') as file:
                    # Load the JSON data
                    data = json.load(file)

                    # Check if the file contains post data
                    if 'media_metadata' in data:
                        # Get the creation timestamp
                        creation_timestamp = data['creation_timestamp']

                        # Convert the creation timestamp to a datetime object
                        date = datetime.fromtimestamp(creation_timestamp)

                        # Get the date in the 'YYYY-MM-DD' format
                        date_str = date.strftime('%Y-%m-%d')

                        # Get the week in the 'Week YYYY-WW' format
                        week_str = f"Week {date.isocalendar()[0]}-{date.isocalendar()[1]}"

                        # Increment the daily post views
                        if date_str in daily_post_views:
                            daily_post_views[date_str] += 1
                        else:
                            daily_post_views[date_str] = 1

                        # Increment the weekly post views
                        if week_str in weekly_post_views:
                            weekly_post_views[week_str] += 1
                        else:
                            weekly_post_views[week_str] = 1

        return daily_post_views, weekly_post_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(daily_post_views, weekly_post_views):
    try:
        # Create the results directory if it does not exist
        results_dir = 'query_responses'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Open the CSV file
        with open(os.path.join(results_dir, 'results.csv'), 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)

            # Write the header
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

            # Write the daily post views
            for date, views in daily_post_views.items():
                writer.writerow([date, views, 'Daily'])

            # Write the weekly post views
            for week, views in weekly_post_views.items():
                writer.writerow([week, views, 'Weekly'])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        daily_post_views, weekly_post_views = get_post_views(root_dir)
        save_to_csv(daily_post_views, weekly_post_views)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()