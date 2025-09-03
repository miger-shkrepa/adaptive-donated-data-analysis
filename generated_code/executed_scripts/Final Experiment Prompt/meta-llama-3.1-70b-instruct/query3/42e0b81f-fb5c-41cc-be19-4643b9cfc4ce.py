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
    A dictionary with timestamps as keys and view counts as values.
    """
    post_views = {}
    
    # Check if the required file exists
    file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            for post in data["impressions_history_posts_seen"]:
                timestamp = post["string_map_data"]["Time"]["timestamp"]
                post_views[timestamp] = post_views.get(timestamp, 0) + 1
    except json.JSONDecodeError:
        raise ValueError("Error: The posts_viewed.json file is not a valid JSON file.")
    
    return post_views

def calculate_daily_and_weekly_views(post_views):
    """
    Calculate daily and weekly post views.
    
    Args:
    post_views (dict): A dictionary with timestamps as keys and view counts as values.
    
    Returns:
    Two dictionaries, one for daily views and one for weekly views.
    """
    daily_views = {}
    weekly_views = {}
    
    for timestamp, views in post_views.items():
        date = datetime.utcfromtimestamp(int(timestamp)).strftime("%Y-%m-%d")
        week = datetime.utcfromtimestamp(int(timestamp)).strftime("Week %Y-%W")
        
        daily_views[date] = daily_views.get(date, 0) + views
        weekly_views[week] = weekly_views.get(week, 0) + views
    
    return daily_views, weekly_views

def write_to_csv(daily_views, weekly_views):
    """
    Write the daily and weekly views to a CSV file.
    
    Args:
    daily_views (dict): A dictionary with daily views.
    weekly_views (dict): A dictionary with weekly views.
    """
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        
        for date, views in daily_views.items():
            writer.writerow([date, views, "Daily"])
        
        for week, views in weekly_views.items():
            writer.writerow([week, views, "Weekly"])

def main():
    try:
        post_views = get_post_views(root_dir)
        daily_views, weekly_views = calculate_daily_and_weekly_views(post_views)
        write_to_csv(daily_views, weekly_views)
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        print(e)
    except Exception as e:
        raise Exception("Error: An unexpected error occurred.") from e

if __name__ == "__main__":
    main()