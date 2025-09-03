import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file and load its contents
        with open(os.path.join(root_dir, filename), "r") as f:
            data = json.load(f)
        
        # Check if the JSON file contains the required structure
        if "ads_information" in data and "instagram_ads_and_businesses" in data["ads_information"]:
            # Extract the topics of interest from the JSON file
            topics_of_interest.extend([topic["value"] for topic in data["ads_information"]["instagram_ads_and_businesses"]["other_categories_used_to_reach_you.json"]["structure"]["label_values"][0]["vec"][0]["value"]])
        
        # Check if the JSON file contains the required structure
        if "personal_information" in data and "information_about_you" in data["personal_information"]:
            # Extract the topics of interest from the JSON file
            topics_of_interest.extend([topic["value"] for topic in data["personal_information"]["information_about_you"]["locations_of_interest.json"]["structure"]["label_values"][0]["vec"][0]["value"]])

# Write the topics of interest to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])
    writer.writerows([[topic] for topic in topics_of_interest])