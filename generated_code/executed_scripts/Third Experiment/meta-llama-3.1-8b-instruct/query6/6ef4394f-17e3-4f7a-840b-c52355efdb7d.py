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
            if 'your_instagram_activity' in data and 'media' in data['your_instagram_activity'] and 'profile_photos.json' in data['your_instagram_activity']['media']:
                # Open the profile_photos.json file
                with open(os.path.join(root_dir, 'your_instagram_activity', 'media', 'profile_photos.json'), 'r') as profile_photos_file:
                    # Load the profile_photos.json data
                    profile_photos_data = eval(profile_photos_file.read())

                    # Iterate over the profile photos
                    for profile_photo in profile_photos_data['ig_profile_picture']:
                        # Extract the creation timestamp
                        creation_timestamp = profile_photo['creation_timestamp']

                        # Extract the cross-post source
                        cross_post_source = profile_photo['cross_post_source']

                        # Extract the media metadata
                        media_metadata = profile_photo['media_metadata']

                        # Extract the camera metadata
                        camera_metadata = media_metadata['camera_metadata']

                        # Extract the has camera metadata
                        has_camera_metadata = camera_metadata['has_camera_metadata']

                        # Extract the URI
                        uri = profile_photo['uri']

                        # Extract the title
                        title = profile_photo['title']

                        # Append the change to the list
                        changes.append((title, uri, datetime.datetime.fromtimestamp(creation_timestamp).strftime('%Y-%m-%d')))

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Changed', 'New Value', 'Change Date'])
    writer.writerows(changes)