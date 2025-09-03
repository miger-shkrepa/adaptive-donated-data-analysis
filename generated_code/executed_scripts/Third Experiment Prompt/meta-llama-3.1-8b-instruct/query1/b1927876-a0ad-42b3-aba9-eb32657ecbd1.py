import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Iterate over the subdirectories in the root directory
for dir_name in os.listdir(root_dir):
    # Check if the subdirectory is a directory
    if os.path.isdir(os.path.join(root_dir, dir_name)):
        # Iterate over the files in the subdirectory
        for file_name in os.listdir(os.path.join(root_dir, dir_name)):
            # Check if the file is a JSON file
            if file_name.endswith(".json"):
                # Open the JSON file and load its contents
                with open(os.path.join(root_dir, dir_name, file_name), "r") as file:
                    data = file.read()
                    # Parse the JSON data
                    import json
                    json_data = json.loads(data)
                    # Check if the JSON data has a 'structure' key
                    if 'structure' in json_data:
                        # Iterate over the items in the 'structure' key
                        for item in json_data['structure']:
                            # Check if the item has a 'title' key
                            if 'title' in item:
                                # Add the title to the topics of interest list
                                topics_of_interest.append(item['title'])

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])
    writer.writerows([topic] for topic in topics_of_interest)