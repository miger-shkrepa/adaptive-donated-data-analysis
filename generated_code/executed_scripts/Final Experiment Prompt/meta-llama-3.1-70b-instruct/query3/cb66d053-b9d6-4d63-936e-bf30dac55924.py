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
    
    # Check if the required file exists
    file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            for post in data["impressions_history_posts_seen"]:
                timestamp = post["string_map_data"]["Time"]["timestamp"]
                date = datetime.fromtimestamp(timestamp)
                date_str = date.strftime("%Y-%m-%d")
                week_str = date.strftime("Week %Y-%W")
                
                # Update daily post views
                if date_str not in post_views:
                    post_views[date_str] = {"Daily": 0, "Weekly": 0}
                post_views[date_str]["Daily"] += 1
                
                # Update weekly post views
                if week_str not in post_views:
                    post_views[week_str] = {"Daily": 0, "Weekly": 0}
                post_views[week_str]["Weekly"] += 1
    except json.JSONDecodeError:
        raise ValueError("Error: Invalid JSON format in the posts_viewed.json file.")
    except KeyError:
        raise ValueError("Error: Invalid JSON structure in the posts_viewed.json file.")
    
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
    try:
        post_views = get_post_views(root_dir)
        save_to_csv(post_views)
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        print(e)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()