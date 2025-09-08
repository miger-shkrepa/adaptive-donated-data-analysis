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

# Iterate over the JSON files
for filename in os.listdir(root_dir):
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = json.load(file)

            # Check if the JSON file contains the required data
            if "profile" in data and "ig_profile_picture" in data["profile"]:
                # Iterate over the profile pictures
                for picture in data["profile"]["ig_profile_picture"]:
                    # Check if the picture has a title and a creation timestamp
                    if "title" in picture and "creation_timestamp" in picture:
                        # Extract the title and creation timestamp
                        title = picture["title"]
                        creation_timestamp = picture["creation_timestamp"]

                        # Convert the creation timestamp to a date
                        date = datetime.datetime.fromtimestamp(creation_timestamp).strftime("%Y-%m-%d")

                        # Add the change to the list
                        changes.append([title, None, date])

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Changed", "New Value", "Change Date"])
    writer.writerows(changes)