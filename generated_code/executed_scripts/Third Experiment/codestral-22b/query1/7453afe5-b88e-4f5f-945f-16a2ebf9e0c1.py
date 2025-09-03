import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store topics of interest
topics_of_interest = []

# Define the path to the interests JSON file
interests_file = os.path.join(root_dir, "logged_information", "interests_from_advertisers.json")

# Check if the interests file exists
if os.path.exists(interests_file):
    # Load the JSON data from the interests file
    with open(interests_file, 'r') as f:
        data = json.load(f)

    # Extract the topics of interest from the JSON data
    for item in data["interests_from_advertisers"]:
        topics_of_interest.append(item["title"])

# Save the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    writer.writerows([[topic] for topic in topics_of_interest])