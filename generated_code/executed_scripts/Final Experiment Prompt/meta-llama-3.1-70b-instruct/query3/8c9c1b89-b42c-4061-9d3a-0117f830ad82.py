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
        raise FileNotFoundError("FileNotFoundError: The required file does not exist.")
    
    try:
        # Load the JSON data
        with open(file_path, "r") as file:
            data = json.load(file)
        
        # Extract the post views data
        for entry in data["impressions_history_posts_seen"]:
            timestamp = entry["string_map_data"]["Time"]["timestamp"]
            date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
            week = datetime.utcfromtimestamp(timestamp).strftime("Week %Y-%W")
            
            # Update the post views data
            if date not in post_views:
                post_views[date] = 1
            else:
                post_views[date] += 1
            
            if week not in post_views:
                post_views[week] = 1
            else:
                post_views[week] += 1
    
    except json.JSONDecodeError:
        raise ValueError("Error: Invalid JSON data.")
    
    except KeyError:
        raise ValueError("Error: Invalid JSON structure.")
    
    return post_views

def save_to_csv(post_views):
    """
    Save the post views data to a CSV file.
    
    Args:
    post_views (dict): A dictionary containing the post views data.
    """
    # Define the CSV file path
    csv_file_path = "query_responses/results.csv"
    
    # Create the directory if it does not exist
    if not os.path.exists("query_responses"):
        os.makedirs("query_responses")
    
    # Save the data to the CSV file
    with open(csv_file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        
        for date, views in post_views.items():
            if date.startswith("Week"):
                writer.writerow([date, views, "Weekly"])
            else:
                writer.writerow([date, views, "Daily"])

def main():
    try:
        post_views = get_post_views(root_dir)
        save_to_csv(post_views)
    
    except FileNotFoundError as e:
        # Save an empty CSV file if the required file does not exist
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])
        print(e)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()