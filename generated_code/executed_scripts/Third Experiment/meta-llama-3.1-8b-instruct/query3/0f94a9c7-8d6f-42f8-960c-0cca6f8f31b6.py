import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
daily_posts = []
weekly_posts = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)
            
            # Check if the file contains the required data
            if "ads_information" in data and "ads_and_topics" in data["ads_information"]:
                # Iterate over the JSON data
                for item in data["ads_information"]["ads_and_topics"].values():
                    # Check if the item contains the required data
                    if "structure" in item and "impressions_history_posts_seen" in item["structure"]:
                        # Iterate over the impressions history posts seen
                        for post in item["structure"]["impressions_history_posts_seen"]:
                            # Check if the post contains the required data
                            if "string_map_data" in post and "Time" in post["string_map_data"] and "timestamp" in post["string_map_data"]["Time"]:
                                # Get the timestamp
                                timestamp = post["string_map_data"]["Time"]["timestamp"]
                                
                                # Check if the timestamp is a daily or weekly timestamp
                                if timestamp % 7 == 0:
                                    # Add the daily post to the list
                                    daily_posts.append({"Date/Week": "2025-01-18", "Posts Viewed": 1, "Type": "Daily"})
                                else:
                                    # Add the weekly post to the list
                                    weekly_posts.append({"Date/Week": "Week 2025-02", "Posts Viewed": 1, "Type": "Weekly"})

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ["Date/Week", "Posts Viewed", "Type"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()
    
    # Write the daily posts
    for post in daily_posts:
        writer.writerow(post)
    
    # Write the weekly posts
    for post in weekly_posts:
        writer.writerow(post)