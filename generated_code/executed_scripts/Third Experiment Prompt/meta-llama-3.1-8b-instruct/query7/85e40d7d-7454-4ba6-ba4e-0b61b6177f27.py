import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = 'query_responses/results.csv'

# Initialize the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])

    # Iterate over the stories directory
    for year in os.listdir(os.path.join(root_dir, "media", "stories")):
        for file in os.listdir(os.path.join(root_dir, "media", "stories", year)):
            if file.endswith(".json"):
                with open(os.path.join(root_dir, "media", "stories", year, file), 'r') as json_file:
                    data = json.load(json_file)
                    for story in data["ig_stories"]:
                        user = story["creation_timestamp"]
                        writer.writerow([user, 1])