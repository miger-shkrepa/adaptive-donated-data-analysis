import csv
import os
import datetime

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
        # Open the file and load its contents
        with open(os.path.join(root_dir, filename), 'r') as file:
            data = file.read()

        # Check if the file contains the required data
        if "impressions_history_posts_seen" in data:
            # Parse the JSON data
            import json
            parsed_data = json.loads(data)

            # Iterate over the impressions history
            for impression in parsed_data["impressions_history_posts_seen"]:
                # Get the timestamp
                timestamp = impression["string_map_data"]["Time"]["timestamp"]

                # Convert the timestamp to a date
                date = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

                # Check if the date is a weekday or a weekend
                if datetime.datetime.fromtimestamp(timestamp).weekday() < 5:
                    # Add the daily post to the list
                    daily_posts.append((date, 1))
                else:
                    # Add the weekly post to the list
                    weekly_posts.append((f"Week {datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%W')}", 1))

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])

    # Write the daily posts to the CSV file
    for post in daily_posts:
        writer.writerow([post[0], post[1], "Daily"])

    # Write the weekly posts to the CSV file
    for post in weekly_posts:
        writer.writerow([post[0], post[1], "Weekly"])