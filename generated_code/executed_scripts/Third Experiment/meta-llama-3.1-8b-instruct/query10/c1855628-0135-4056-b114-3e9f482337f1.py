import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the counters
post_views = 0
video_views = 0

# Initialize the set of accounts
accounts = set()

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if "impressions_history_ads_seen" in data["ads_and_topics"][filename]:
                # Iterate over the impressions history
                for impression in data["ads_and_topics"][filename]["impressions_history_ads_seen"]:
                    # Increment the post views counter
                    post_views += 1
                    # Add the account to the set of accounts
                    accounts.add(impression["string_map_data"]["Author"]["value"])

            elif "impressions_history_app_message" in data["ads_and_topics"][filename]:
                # Iterate over the impressions history
                for impression in data["ads_and_topics"][filename]["impressions_history_app_message"]:
                    # Increment the post views counter
                    post_views += 1
                    # Add the account to the set of accounts
                    accounts.add(impression["string_map_data"]["Author"]["value"])

            elif "impressions_history_posts_seen" in data["ads_and_topics"][filename]:
                # Iterate over the impressions history
                for impression in data["ads_and_topics"][filename]["impressions_history_posts_seen"]:
                    # Increment the post views counter
                    post_views += 1
                    # Add the account to the set of accounts
                    accounts.add(impression["string_map_data"]["Author"]["value"])

            elif "impressions_history_videos_watched" in data["ads_and_topics"][filename]:
                # Iterate over the impressions history
                for impression in data["ads_and_topics"][filename]["impressions_history_videos_watched"]:
                    # Increment the video views counter
                    video_views += 1
                    # Add the account to the set of accounts
                    accounts.add(impression["string_map_data"]["Author"]["value"])

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])
    for account in accounts:
        writer.writerow([account, post_views, video_views])

print("The CSV file has been created successfully.")