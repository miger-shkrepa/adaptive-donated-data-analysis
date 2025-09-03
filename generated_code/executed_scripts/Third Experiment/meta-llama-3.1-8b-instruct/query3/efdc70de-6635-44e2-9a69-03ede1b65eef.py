import csv
import os
import datetime

# Declare the root directory variable
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
            data = file.read()
            # Check if the JSON data contains the required structure
            if "policy_updates_and_permissions" in data:
                # Parse the JSON data
                import json
                json_data = json.loads(data)
                # Check if the JSON data contains the required keys
                if "notification_of_privacy_policy_updates.json" in json_data["policy_updates_and_permissions"]:
                    # Parse the JSON data
                    json_data = json_data["policy_updates_and_permissions"]["notification_of_privacy_policy_updates.json"]
                    # Check if the JSON data contains the required structure
                    if "string_map_data" in json_data[0]:
                        # Parse the JSON data
                        json_data = json_data[0]["string_map_data"]
                        # Check if the JSON data contains the required keys
                        if "Impression Time" in json_data and "Consent Status" in json_data:
                            # Get the impression time and consent status
                            impression_time = json_data["Impression Time"]["value"]
                            consent_status = json_data["Consent Status"]["value"]
                            # Check if the impression time is a date
                            if datetime.datetime.strptime(impression_time, "%Y-%m-%d"):
                                # Add the daily post to the list
                                daily_posts.append((impression_time, 1, "Daily"))
                            # Check if the impression time is a week
                            elif datetime.datetime.strptime(impression_time, "%Y-W%W"):
                                # Add the weekly post to the list
                                weekly_posts.append((impression_time, 1, "Weekly"))

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    # Write the daily posts
    for post in daily_posts:
        writer.writerow(post)
    # Write the weekly posts
    for post in weekly_posts:
        writer.writerow(post)