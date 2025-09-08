import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the changes
changes = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if "your_instagram_activity" in data and "content" in data["your_instagram_activity"] and "profile_photos.json" in data["your_instagram_activity"]["content"]:
                # Load the profile photos data
                profile_photos_data = data["your_instagram_activity"]["content"]["profile_photos.json"]

                # Iterate over the profile photos
                for profile_photo in profile_photos_data["ig_profile_picture"]:
                    # Check if the profile photo contains the required information
                    if "title" in profile_photo and "backup_uri" in profile_photo and "creation_timestamp" in profile_photo:
                        # Extract the title, backup URI, and creation timestamp
                        title = profile_photo["title"]
                        backup_uri = profile_photo["backup_uri"]
                        creation_timestamp = profile_photo["creation_timestamp"]

                        # Convert the creation timestamp to a date string
                        date_string = datetime.datetime.fromtimestamp(creation_timestamp).strftime("%Y-%m-%d")

                        # Add the change to the list
                        changes.append([title, backup_uri, date_string])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)