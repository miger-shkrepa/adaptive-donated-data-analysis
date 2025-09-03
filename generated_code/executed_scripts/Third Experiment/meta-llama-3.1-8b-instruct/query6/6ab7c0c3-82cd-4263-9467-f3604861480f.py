import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of changes
changes = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains Instagram account changes
            if "your_instagram_activity" in data and "comments" in data["your_instagram_activity"] and "post_comments_1.json" in data["your_instagram_activity"]["comments"]:
                # Iterate over the comments
                for comment in data["your_instagram_activity"]["comments"]["post_comments_1.json"]["structure"]:
                    # Check if the comment contains a name, phone, or email change
                    if "string_map_data" in comment and ("Name" in comment["string_map_data"] or "Phone" in comment["string_map_data"] or "Email" in comment["string_map_data"]):
                        # Extract the change
                        change = {}
                        if "Name" in comment["string_map_data"]:
                            change["Changed"] = "Name"
                            change["New Value"] = comment["string_map_data"]["Name"]["value"]
                        elif "Phone" in comment["string_map_data"]:
                            change["Changed"] = "Phone"
                            change["New Value"] = comment["string_map_data"]["Phone"]["value"]
                        elif "Email" in comment["string_map_data"]:
                            change["Changed"] = "Email"
                            change["New Value"] = comment["string_map_data"]["Email"]["value"]
                        change["Change Date"] = datetime.datetime.now().strftime("%Y-%m-%d")
                        changes.append(change)

# Write the changes to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Changed', 'New Value', 'Change Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for change in changes:
        writer.writerow(change)