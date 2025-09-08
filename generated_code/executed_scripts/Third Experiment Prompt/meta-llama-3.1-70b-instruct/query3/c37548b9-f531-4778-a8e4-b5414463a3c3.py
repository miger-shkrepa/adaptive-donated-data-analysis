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

        # Iterate over media directories
        media_dir = os.path.join(root_dir, "media")
        if os.path.exists(media_dir):
            for media_type in os.listdir(media_dir):
                media_type_dir = os.path.join(media_dir, media_type)
                if os.path.isdir(media_type_dir):
                    for date_dir in os.listdir(media_type_dir):
                        date_dir_path = os.path.join(media_type_dir, date_dir)
                        if os.path.isdir(date_dir_path):
                            # Get date from directory name
                            try:
                                date = datetime.strptime(date_dir, "%Y%m%d")
                                date_str = date.strftime("%Y-%m-%d")
                                week_str = "Week " + date.strftime("%Y-%W")
                            except ValueError:
                                # Handle invalid date format
                                continue

                            # Count post views for the day
                            daily_post_views[date_str] = daily_post_views.get(date_str, 0) + len(os.listdir(date_dir_path))

                            # Count post views for the week
                            weekly_post_views[week_str] = weekly_post_views.get(week_str, 0) + len(os.listdir(date_dir_path))

        # Write post views to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["Date/Week", "Posts Viewed", "Type"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            # Write daily post views
            for date, views in daily_post_views.items():
                writer.writerow({"Date/Week": date, "Posts Viewed": views, "Type": "Daily"})

            # Write weekly post views
            for week, views in weekly_post_views.items():
                writer.writerow({"Date/Week": week, "Posts Viewed": views, "Type": "Weekly"})

    except Exception as e:
        # Handle any exceptions
        print(f"Error: {str(e)}")

        # Write column headers to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            fieldnames = ["Date/Week", "Posts Viewed", "Type"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

get_post_views(root_dir)