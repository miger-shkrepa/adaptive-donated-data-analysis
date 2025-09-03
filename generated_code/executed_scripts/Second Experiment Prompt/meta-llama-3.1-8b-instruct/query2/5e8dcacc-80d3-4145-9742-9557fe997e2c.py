import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the ads_information directory
ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
if os.path.exists(ads_info_dir):
    for file in os.listdir(ads_info_dir):
        # Check if the file is a JSON file
        if file.endswith(".json"):
            # Open the JSON file
            with open(os.path.join(ads_info_dir, file), "r") as f:
                # Load the JSON data
                data = json.load(f)
                # Extract the company name and number of ads viewed
                company_name = file.replace(".json", "")
                num_ads_viewed = len(data["structure"]["impressions_history_ads_seen"])
                # Append the result to the list
                results.append((company_name, num_ads_viewed))

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(results)