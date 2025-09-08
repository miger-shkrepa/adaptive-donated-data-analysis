import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
accounts = []
post_views = []
video_views = []

# Iterate over the JSON files in the 'your_instagram_activity' directory
for account in os.listdir(root_dir):
    if account == 'your_instagram_activity':
        for file in os.listdir(os.path.join(root_dir, account)):
            if file.endswith('.json'):
                # Open the JSON file
                with open(os.path.join(root_dir, account, file), 'r') as f:
                    # Load the JSON data
                    data = eval(f.read())

                    # Check if the file contains the required data
                    if 'likes' in data and 'saved' in data:
                        # Iterate over the likes and saved posts
                        for post in data['likes']['liked_posts.json']['structure']['likes_media_likes']:
                            # Increment the post views
                            post_views.append(1)
                            # Get the account name from the file name
                            account_name = file.split('.')[0]
                            accounts.append(account_name)

                        for post in data['saved']['saved_posts.json']['structure']['saved_saved_media']:
                            # Increment the video views
                            video_views.append(1)
                            # Get the account name from the file name
                            account_name = file.split('.')[0]
                            accounts.append(account_name)

# Write the data to the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Account', 'Post Views', 'Video Views'])
    for i in range(len(accounts)):
        writer.writerow([accounts[i], post_views[i], video_views[i]])