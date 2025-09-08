import os
import json
import csv
from datetime import datetime, timedelta
from collections import defaultdict

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

# Initialize dictionaries to store daily and weekly post views
daily_views = defaultdict(int)
weekly_views = defaultdict(int)

# Traverse the directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "recently_viewed_items.json":
            filepath = os.path.join(dirpath, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                for item in data["checkout_saved_recently_viewed_products"]:
                    # Assuming the timestamp is in the "Product Name" field
                    # This is a guess based on the structure provided
                    timestamp_str = item["string_map_data"]["Product Name"]["value"]
                    try:
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d')
                        daily_views[timestamp.strftime('%Y-%m-%d')] += 1
                        weekly_views[f'Week {timestamp.strftime("%Y-%W")}'] += 1
                    except ValueError:
                        print(f"Error: Invalid timestamp format in {filepath}")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])
    for date, views in daily_views.items():
        writer.writerow([date, views, 'Daily'])
    for week, views in weekly_views.items():
        writer.writerow([week, views, 'Weekly'])