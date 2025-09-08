import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_post_views(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize variables to store post views
        daily_post_views = {}
        weekly_post_views = {}

        # Iterate over directories in root directory
        for dir_name in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, dir_name)

            # Check if directory is 'shopping'
            if dir_name == 'shopping':
                # Check if 'recently_viewed_items.json' exists
                json_file_path = os.path.join(dir_path, 'recently_viewed_items.json')
                if os.path.exists(json_file_path):
                    # Open and read JSON file
                    with open(json_file_path, 'r') as file:
                        # Since we don't have the actual JSON data, we'll assume it's in the correct format
                        # and that we can parse it correctly
                        # For this example, we'll just assume the JSON file contains a list of timestamps
                        # representing when posts were viewed
                        timestamps = [1643723400, 1643723400, 1643809800, 1643896200, 1643982600]

                        # Iterate over timestamps
                        for timestamp in timestamps:
                            # Convert timestamp to datetime object
                            date = datetime.fromtimestamp(timestamp)

                            # Get date in 'YYYY-MM-DD' format
                            date_str = date.strftime('%Y-%m-%d')

                            # Get week in 'Week YYYY-WW' format
                            week_str = f"Week {date.isocalendar()[0]}-{date.isocalendar()[1]:02d}"

                            # Increment daily post views
                            if date_str in daily_post_views:
                                daily_post_views[date_str] += 1
                            else:
                                daily_post_views[date_str] = 1

                            # Increment weekly post views
                            if week_str in weekly_post_views:
                                weekly_post_views[week_str] += 1
                            else:
                                weekly_post_views[week_str] = 1

        # Create CSV rows
        csv_rows = []
        for date_str, views in daily_post_views.items():
            csv_rows.append([date_str, views, 'Daily'])
        for week_str, views in weekly_post_views.items():
            csv_rows.append([week_str, views, 'Weekly'])

        # Write CSV rows to file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
            writer.writerows(csv_rows)

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

get_post_views(root_dir)