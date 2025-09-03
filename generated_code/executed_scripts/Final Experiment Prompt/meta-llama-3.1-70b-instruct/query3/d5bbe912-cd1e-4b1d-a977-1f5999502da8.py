import json
import os
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

def get_post_views(root_dir):
    """
    Extract post views from the impressions_history_posts_seen data.

    Args:
    root_dir (str): The path to the root directory.

    Returns:
    dict: A dictionary containing the post views data.
    """
    post_views = {}
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Check if the posts_viewed.json file exists
        posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
        if not os.path.exists(posts_viewed_file):
            return post_views

        # Load the posts_viewed.json file
        with open(posts_viewed_file, "r") as file:
            data = json.load(file)

        # Extract the post views data
        for post in data.get("impressions_history_posts_seen", []):
            timestamp = post.get("string_map_data", {}).get("Time", {}).get("timestamp")
            if timestamp is not None:
                date = datetime.fromtimestamp(int(timestamp))
                date_str = date.strftime("%Y-%m-%d")
                week_str = date.strftime("Week %Y-%W")

                # Update the post views data
                if date_str not in post_views:
                    post_views[date_str] = {"Daily": 0, "Weekly": 0}
                if week_str not in post_views:
                    post_views[week_str] = {"Daily": 0, "Weekly": 0}

                post_views[date_str]["Daily"] += 1
                post_views[week_str]["Weekly"] += 1

    except json.JSONDecodeError:
        raise ValueError("Error: Failed to parse the JSON file.")

    return post_views

def save_to_csv(post_views):
    """
    Save the post views data to a CSV file.

    Args:
    post_views (dict): A dictionary containing the post views data.
    """
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])

        for date, views in post_views.items():
            if "Daily" in views:
                writer.writerow([date, views["Daily"], "Daily"])
            if "Weekly" in views:
                writer.writerow([date, views["Weekly"], "Weekly"])

def main():
    post_views = get_post_views(root_dir)
    if not post_views:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    else:
        save_to_csv(post_views)

if __name__ == "__main__":
    main()