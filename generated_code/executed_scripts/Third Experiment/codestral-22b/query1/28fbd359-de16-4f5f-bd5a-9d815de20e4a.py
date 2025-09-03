import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

topics_of_interest = []

try:
    with open(os.path.join(root_dir, "information_about_you", "locations_of_interest.json")) as f:
        data = json.load(f)
        for item in data["label_values"]:
            topics_of_interest.append(item["label"])
except FileNotFoundError:
    pass

with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])