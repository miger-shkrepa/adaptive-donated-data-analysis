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

        # Iterate over all files in the directory
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                # Check if file is a video or image file
                if file_name.endswith(('.mp4', '.jpg', '.srt', '.png')):
                    # Get the date from the file name
                    date_str = file_name.split('_')[0]
                    try:
                        date = datetime.strptime(date_str, '%Y%m')
                    except ValueError:
                        try:
                            date = datetime.strptime(date_str, '%Y')
                        except ValueError:
                            continue

                    # Update daily post views
                    date_str_daily = date.strftime('%Y-%m-%d')
                    if date_str_daily not in daily_post_views:
                        daily_post_views[date_str_daily] = 1
                    else:
                        daily_post_views[date_str_daily] += 1

                    # Update weekly post views
                    date_str_weekly = f"Week {date.strftime('%Y-%U')}"
                    if date_str_weekly not in weekly_post_views:
                        weekly_post_views[date_str_weekly] = 1
                    else:
                        weekly_post_views[date_str_weekly] += 1

        return daily_post_views, weekly_post_views

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_to_csv(daily_post_views, weekly_post_views):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for date, views in daily_post_views.items():
                writer.writerow({'Date/Week': date, 'Posts Viewed': views, 'Type': 'Daily'})
            for week, views in weekly_post_views.items():
                writer.writerow({'Date/Week': week, 'Posts Viewed': views, 'Type': 'Weekly'})

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        daily_post_views, weekly_post_views = get_post_views(root_dir)
        write_to_csv(daily_post_views, weekly_post_views)
    except Exception as e:
        print("Error: " + str(e))
        # Write column headers to CSV file if an error occurs
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Date/Week', 'Posts Viewed', 'Type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

if __name__ == "__main__":
    main()