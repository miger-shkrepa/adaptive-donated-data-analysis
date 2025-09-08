import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Account", "Post Views", "Video Views"])

    # Iterate over the 'your_activity_across_facebook' directory
    for account in os.listdir(os.path.join(root_dir, "your_activity_across_facebook", "messages", "inbox")):
        post_views = 0
        video_views = 0

        # Iterate over the 'message_1.json' files in the account directory
        for file in os.listdir(os.path.join(root_dir, "your_activity_across_facebook", "messages", "inbox", account)):
            if file.endswith(".json"):
                with open(os.path.join(root_dir, "your_activity_across_facebook", "messages", "inbox", account, file), 'r') as json_file:
                    data = json.load(json_file)

                    # Check if the file contains post views
                    if "messages" in data and any(message["is_geoblocked_for_viewer"] is False for message in data["messages"]):
                        post_views += len(data["messages"])

                    # Check if the file contains video views
                    if "photos" in data and any(photo["creation_timestamp"] is not None for photo in data["photos"]):
                        video_views += len(data["photos"])

        # Write the account and view counts to the CSV file
        writer.writerow([account, post_views, video_views])