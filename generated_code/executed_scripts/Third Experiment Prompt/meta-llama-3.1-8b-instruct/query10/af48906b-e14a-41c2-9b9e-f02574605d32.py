import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Iterate over the 'media' directory
    for root, dirs, files in os.walk(os.path.join(root_dir, "media")):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)

                try:
                    with open(filepath, 'r') as file:
                        data = json.load(file)

                        # Check if the file is a 'posts' or 'reels' file
                        if "posts" in data and "ig_other_media" in data["posts"]:
                            post_views = len(data["posts"]["ig_other_media"])
                        elif "reels" in data and "ig_reels_media" in data["reels"]:
                            video_views = len(data["reels"]["ig_reels_media"])
                        else:
                            post_views = 0
                            video_views = 0

                        # Get the account name from the directory path
                        account = os.path.basename(os.path.dirname(filepath))

                        # Write the post and video views for the current account to the CSV file
                        writer.writerow([account, post_views, video_views])

                except json.JSONDecodeError:
                    # If the file is not a valid JSON file, skip it
                    continue
                except Exception as e:
                    # If any other error occurs, print the error message
                    print(f"Error: {e}")