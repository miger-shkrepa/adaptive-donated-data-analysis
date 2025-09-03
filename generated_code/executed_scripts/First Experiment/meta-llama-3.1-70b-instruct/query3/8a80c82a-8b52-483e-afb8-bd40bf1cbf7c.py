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
                        if "story_activities" in data or "story_activities_emoji_sliders" in data or "story_activities_polls" in data or "story_activities_questions" in data or "story_activities_quizzes" in data or "story_activities_story_likes" in data:
                            # Extract the timestamp from the post data
                            for post in data.values():
                                if isinstance(post, list):
                                    for item in post:
                                        if "timestamp" in item:
                                            timestamp = item["timestamp"]
                                            date = datetime.fromtimestamp(timestamp)

                                            # Update daily post views
                                            date_str = date.strftime("%Y-%m-%d")
                                            if date_str in daily_post_views:
                                                daily_post_views[date_str] += 1
                                            else:
                                                daily_post_views[date_str] = 1

                                            # Update weekly post views
                                            week_str = f"Week {date.strftime('%Y-%U')}"
                                            if week_str in weekly_post_views:
                                                weekly_post_views[week_str] += 1
                                            else:
                                                weekly_post_views[week_str] = 1

                    except json.JSONDecodeError:
                        raise ValueError("ValueError: Failed to parse JSON file.")

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

    return daily_post_views, weekly_post_views


def save_to_csv(daily_post_views, weekly_post_views):
    try:
        # Create the output CSV file
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

            # Write daily post views to the CSV file
            for date, views in daily_post_views.items():
                writer.writerow([date, views, "Daily"])

            # Write weekly post views to the CSV file
            for week, views in weekly_post_views.items():
                writer.writerow([week, views, "Weekly"])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def main():
    try:
        daily_post_views, weekly_post_views = get_post_views(root_dir)
        save_to_csv(daily_post_views, weekly_post_views)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {str(e)}")
    except ValueError as e:
        raise ValueError(f"ValueError: {str(e)}")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


if __name__ == "__main__":
    main()