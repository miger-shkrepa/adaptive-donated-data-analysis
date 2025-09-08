import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize variables to store the data
account_views = {}
video_views = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON file contains the required data
            if "media" in data and "posts" in data["media"]:
                # Iterate over the posts
                for post in data["media"]["posts"].values():
                    # Check if the post has a title and a creation timestamp
                    if "title" in post and "creation_timestamp" in post:
                        # Get the account name from the title
                        account = post["title"].split("_")[0]

                        # Check if the account is already in the dictionary
                        if account not in account_views:
                            account_views[account] = 0
                        if account not in video_views:
                            video_views[account] = 0

                        # Increment the view count for the account
                        account_views[account] += 1

            elif "media" in data and "other" in data["media"] and "202504" in data["media"]["other"]:
                # Iterate over the media files
                for media in data["media"]["other"]["202504"].values():
                    # Check if the media file has a title and a creation timestamp
                    if "title" in media and "creation_timestamp" in media:
                        # Get the account name from the title
                        account = media["title"].split("_")[0]

                        # Check if the account is already in the dictionary
                        if account not in account_views:
                            account_views[account] = 0
                        if account not in video_views:
                            video_views[account] = 0

                        # Increment the view count for the account
                        account_views[account] += 1

# Create a CSV file to store the results
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Write the data to the CSV file
    for account, views in account_views.items():
        # Check if the account has video views
        video_views_account = video_views.get(account, 0)

        # Write the data to the CSV file
        writer.writerow([account, views, video_views_account])