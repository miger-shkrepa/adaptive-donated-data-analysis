import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = 'query_responses/results.csv'

# Initialize the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])

    # Iterate over the 'connections' directory
    connections_dir = os.path.join(root_dir, "connections")
    if os.path.exists(connections_dir):
        for filename in os.listdir(connections_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(connections_dir, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    if "close_friends.json" in filename:
                        for item in data["relationships_close_friends"]:
                            user = item["title"]
                            times_engaged = len(item["string_list_data"])
                            writer.writerow([user, times_engaged])
                    elif "followers_1.json" in filename:
                        for item in data["relationships_followers"]:
                            user = item["title"]
                            times_engaged = len(item["string_list_data"])
                            writer.writerow([user, times_engaged])
                    elif "following.json" in filename:
                        for item in data["relationships_following"]:
                            user = item["title"]
                            times_engaged = len(item["string_list_data"])
                            writer.writerow([user, times_engaged])
                    elif "hide_story_from.json" in filename:
                        for item in data["relationships_hide_stories_from"]:
                            user = item["title"]
                            times_engaged = len(item["string_list_data"])
                            writer.writerow([user, times_engaged])
                    elif "removed_suggestions.json" in filename:
                        for item in data["relationships_dismissed_suggested_users"]:
                            user = item["title"]
                            times_engaged = len(item["string_list_data"])
                            writer.writerow([user, times_engaged])
                    elif "restricted_accounts.json" in filename:
                        for item in data["relationships_restricted_users"]:
                            user = item["title"]
                            times_engaged = len(item["string_list_data"])
                            writer.writerow([user, times_engaged])
    else:
        writer.writerow(["User", "Times Engaged"])