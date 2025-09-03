import os
import json
import csv
from datetime import datetime, timedelta

# Declare the root directory variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = [["Date/Week", "Posts Viewed", "Type"]]

# Iterate over all the directories in the root directory
for dir_name in os.listdir(root_dir):
    dir_path = os.path.join(root_dir, dir_name)

    # Check if the path is a directory
    if os.path.isdir(dir_path):
        # Iterate over all the JSON files in the directory
        for file_name in os.listdir(dir_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(dir_path, file_name)

                # Open the JSON file
                with open(file_path, "r") as f:
                    data = json.load(f)

                # Check if the JSON file has the required structure
                if "structure" in data and "messages" in data["structure"]:
                    messages = data["structure"]["messages"]

                    # Initialize the daily and weekly post counts
                    daily_counts = {}
                    weekly_counts = {}

                    # Iterate over all the messages
                    for message in messages:
                        # Check if the message has a timestamp
                        if "timestamp_ms" in message:
                            timestamp = int(message["timestamp_ms"])
                            date = datetime.fromtimestamp(timestamp / 1000)

                            # Calculate the daily post count
                            daily_date = date.strftime("%Y-%m-%d")
                            if daily_date in daily_counts:
                                daily_counts[daily_date] += 1
                            else:
                                daily_counts[daily_date] = 1

                            # Calculate the weekly post count
                            weekly_date = date.strftime("Week %Y-%W")
                            if weekly_date in weekly_counts:
                                weekly_counts[weekly_date] += 1
                            else:
                                weekly_counts[weekly_date] = 1

                    # Add the daily post counts to the results list
                    for date, count in daily_counts.items():
                        results.append([date, count, "Daily"])

                    # Add the weekly post counts to the results list
                    for date, count in weekly_counts.items():
                        results.append([date, count, "Weekly"])

# Save the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(results)