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

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Check if the JSON data contains the required information
            if "ig_archived_post_media" in data:
                # Extract the post views
                post_views.append(1)
                accounts.append(filename.split('.')[0])
            elif "ig_secret_conversations" in data:
                # Extract the video views
                video_views.append(1)
                accounts.append(filename.split('.')[0])
            elif "monetization_eligibility" in data:
                # Extract the video views
                video_views.append(1)
                accounts.append(filename.split('.')[0])

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(["Account", "Post Views", "Video Views"])
    # Write the data
    for i in range(len(accounts)):
        writer.writerow([accounts[i], post_views[i], video_views[i]])

# Check if the necessary files or directories do not exist
if len(accounts) == 0:
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Account", "Post Views", "Video Views"])