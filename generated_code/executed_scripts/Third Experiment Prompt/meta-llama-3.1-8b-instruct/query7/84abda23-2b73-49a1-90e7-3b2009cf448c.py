import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the results list
results = []

# Iterate over the 'your_activity_across_facebook' directory
for user in os.listdir(os.path.join(root_dir, "your_activity_across_facebook", "messages", "inbox")):
    # Skip non-json files
    if not user.endswith(".json"):
        continue

    # Load the JSON file
    with open(os.path.join(root_dir, "your_activity_across_facebook", "messages", "inbox", user), "r") as f:
        data = json.load(f)

    # Extract the user name
    user_name = data["title"]

    # Initialize the engagement count
    engagement_count = 0

    # Iterate over the messages
    for message in data["messages"]:
        # Check if the message is a story
        if "media" in message and message["media"]:
            # Increment the engagement count
            engagement_count += 1

    # Append the result to the list
    results.append((user_name, engagement_count))

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Times Engaged"])
    writer.writerows(results)