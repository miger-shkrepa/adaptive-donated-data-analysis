import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except FileNotFoundError as e:
    print(e)
    exit()

# Initialize the output CSV file
output_csv = "query_responses/results.csv"

# Initialize the CSV writer
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Iterate over the 'your_instagram_activity' directory
    for account in os.listdir(root_dir + "/your_instagram_activity"):
        account_path = root_dir + "/your_instagram_activity/" + account
        if os.path.isdir(account_path):
            post_views = 0
            video_views = 0

            # Iterate over the 'likes' and 'saved' directories
            for content_type in os.listdir(account_path):
                content_path = account_path + "/" + content_type
                if os.path.isdir(content_path):
                    for file in os.listdir(content_path):
                        file_path = content_path + "/" + file
                        if file.endswith(".json"):
                            with open(file_path, 'r') as json_file:
                                data = json.load(json_file)
                                if content_type == "likes":
                                    for post in data["structure"]["likes_media_likes"]:
                                        post_views += len(post["string_list_data"])
                                elif content_type == "saved":
                                    for post in data["structure"]["saved_saved_media"]:
                                        video_views += 1

            # Write the account data to the CSV file
            writer.writerow([account, post_views, video_views])