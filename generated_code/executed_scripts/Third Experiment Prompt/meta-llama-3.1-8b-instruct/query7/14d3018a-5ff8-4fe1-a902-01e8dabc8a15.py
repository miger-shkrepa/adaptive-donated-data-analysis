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
            if filename == "close_friends.json":
                close_friends_file = os.path.join(connections_dir, filename)
                with open(close_friends_file, 'r') as json_file:
                    close_friends_data = json.load(json_file)
                    for item in close_friends_data["structure"][0]["string_list_data"]:
                        user = item["value"]
                        writer.writerow([user, 1])
    else:
        writer.writerow(["User", "Times Engaged"])

    # Iterate over the 'your_instagram_activity' directory
    your_instagram_activity_dir = os.path.join(root_dir, "your_instagram_activity")
    if os.path.exists(your_instagram_activity_dir):
        for filename in os.listdir(your_instagram_activity_dir):
            if filename == "stories.json":
                stories_file = os.path.join(your_instagram_activity_dir, filename)
                with open(stories_file, 'r') as json_file:
                    stories_data = json.load(json_file)
                    for item in stories_data["structure"]:
                        user = item["title"]
                        writer.writerow([user, 1])
    else:
        writer.writerow(["User", "Times Engaged"])

# Close the CSV writer
csvfile.close()