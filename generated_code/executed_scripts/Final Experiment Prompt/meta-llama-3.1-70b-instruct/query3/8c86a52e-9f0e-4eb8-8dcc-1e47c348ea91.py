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
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")

        # Load the posts_viewed.json file
        with open(posts_viewed_file, "r") as file:
            data = json.load(file)

        # Extract the post views data
        for post in data.get("impressions_history_posts_seen", []):
            timestamp = post.get("string_map_data", {}).get("Time", {}).get("timestamp")
            if timestamp:
                date = datetime.utcfromtimestamp(int(timestamp)).strftime("%Y-%m-%d")
                week = datetime.utcfromtimestamp(int(timestamp)).strftime("Week %Y-%W")
                post_views[date] = post_views.get(date, 0) + 1
                post_views[week] = post_views.get(week, 0) + 1

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Failed to parse JSON - {e}")

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

    return post_views

def save_to_csv(post_views):
    """
    Save the post views data to a CSV file.

    Args:
    post_views (dict): A dictionary containing the post views data.
    """
    try:
        # Create the results directory if it does not exist
        results_dir = "query_responses"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Save the post views data to a CSV file
        with open(os.path.join(results_dir, "results.csv"), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
            for date, views in post_views.items():
                if date.startswith("Week"):
                    writer.writerow([date, views, "Weekly"])
                else:
                    writer.writerow([date, views, "Daily"])

    except Exception as e:
        raise ValueError(f"ValueError: Failed to save to CSV - {e}")

def main():
    try:
        post_views = get_post_views(root_dir)
        save_to_csv(post_views)

    except FileNotFoundError as e:
        # Save a CSV file with only the column headers if a required file does not exist
        with open(os.path.join("query_responses", "results.csv"), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        print(f"Error: {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()