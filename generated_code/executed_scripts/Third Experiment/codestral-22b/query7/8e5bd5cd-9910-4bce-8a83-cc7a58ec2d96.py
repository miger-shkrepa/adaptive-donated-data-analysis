import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

stories_file = os.path.join(root_dir, "personal_information", "device_information", "stories.json")

if not os.path.exists(stories_file):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
else:
    with open(stories_file, 'r') as f:
        data = json.load(f)

    # Since the data does not contain information about who the user is engaging with,
    # we cannot answer the query using the available data.
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])