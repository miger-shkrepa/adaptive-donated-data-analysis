import os
import json
import csv
from datetime import datetime, timedelta

# Define the root directory
root_dir = "root_dir"

# Function to parse JSON files and extract relevant data
def parse_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")

# Function to process the directory and extract post view data
def process_directory(root_dir):
    post_views = []

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Define the path to the recently_viewed_items.json file
    recently_viewed_items_path = os.path.join(root_dir, "shopping", "recently_viewed_items.json")

    # Check if the recently_viewed_items.json file exists
    if os.path.exists(recently_viewed_items_path):
        data = parse_json_file(recently_viewed_items_path)
        for item in data.get("checkout_saved_recently_viewed_products", []):
            post_views.append(item)

    return post_views

# Function to aggregate post views by day and week
def aggregate_post_views(post_views):
    daily_views = {}
    weekly_views = {}

    for view in post_views:
        # Assuming the timestamp is in milliseconds
        timestamp = view.get("timestamp", 0) / 1000
        date = datetime.fromtimestamp(timestamp)
        date_str = date.strftime("%Y-%m-%d")
        week_str = f"Week {date.strftime('%Y-%W')}"

        if date_str in daily_views:
            daily_views[date_str] += 1
        else:
            daily_views[date_str] = 1

        if week_str in weekly_views:
            weekly_views[week_str] += 1
        else:
            weekly_views[week_str] = 1

    return daily_views, weekly_views

# Function to write the results to a CSV file
def write_to_csv(daily_views, weekly_views):
    output_path = "query_responses/results.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ["Date/Week", "Posts Viewed", "Type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for date, count in daily_views.items():
            writer.writerow({"Date/Week": date, "Posts Viewed": count, "Type": "Daily"})

        for week, count in weekly_views.items():
            writer.writerow({"Date/Week": week, "Posts Viewed": count, "Type": "Weekly"})

# Main function to execute the script
def main():
    try:
        post_views = process_directory(root_dir)
        daily_views, weekly_views = aggregate_post_views(post_views)
        write_to_csv(daily_views, weekly_views)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()