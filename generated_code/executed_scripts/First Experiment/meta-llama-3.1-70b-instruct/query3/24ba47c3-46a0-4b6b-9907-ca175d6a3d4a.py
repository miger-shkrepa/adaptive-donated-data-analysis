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

        # Iterate over the directory structure
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                # Check if the file is a JSON file
                if file_name.endswith(".json"):
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        # Open and load the JSON file
                        with open(file_path, "r") as file:
                            data = json.load(file)

                        # Check if the file contains post data
                        if "creation_timestamp" in data:
                            # Get the post date
                            post_date = datetime.fromtimestamp(data["creation_timestamp"])

                            # Update daily views
                            date_key = post_date.strftime("%Y-%m-%d")
                            if date_key in daily_views:
                                daily_views[date_key] += 1
                            else:
                                daily_views[date_key] = 1

                            # Update weekly views
                            week_key = f"Week {post_date.strftime('%Y-%U')}"
                            if week_key in weekly_views:
                                weekly_views[week_key] += 1
                            else:
                                weekly_views[week_key] = 1

                    except json.JSONDecodeError:
                        raise ValueError("ValueError: Invalid JSON file.")

        return daily_views, weekly_views

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(daily_views, weekly_views):
    try:
        # Create the output directory if it does not exist
        output_dir = "query_responses"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the data to a CSV file
        with open(os.path.join(output_dir, "results.csv"), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

            # Write daily views
            for date, views in daily_views.items():
                writer.writerow([date, views, "Daily"])

            # Write weekly views
            for week, views in weekly_views.items():
                writer.writerow([week, views, "Weekly"])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        daily_views, weekly_views = get_post_views(root_dir)
        save_to_csv(daily_views, weekly_views)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()