import json
import csv
import os

# Declare the root directory
root_dir = "root_dir"

# Initialize an empty dictionary to store the results
results = {}

# Construct the path to the JSON file
json_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

# Check if the file exists
if not os.path.isfile(json_file_path):
    # If the file does not exist, create an empty CSV file with only the column headers
    with open("query_responses/results.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
else:
    # Open the JSON file
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # Check if the JSON data is a dictionary
    if not isinstance(data, dict):
        raise ValueError("ValueError: The JSON file does not contain a dictionary.")

    # Check if the JSON data contains the "impressions_history_ads_seen" key
    if "impressions_history_ads_seen" not in data:
        raise ValueError("ValueError: The JSON file does not contain the 'impressions_history_ads_seen' key.")

    # Iterate over the "impressions_history_ads_seen" list
    for ad in data["impressions_history_ads_seen"]:
        # Check if the "string_map_data" key exists in the ad dictionary
        if "string_map_data" not in ad:
            continue

        # Check if the "Author" key exists in the "string_map_data" dictionary
        if "Author" not in ad["string_map_data"]:
            continue

        # Check if the "value" key exists in the "Author" dictionary
        if "value" not in ad["string_map_data"]["Author"]:
            continue

        # Extract the company name
        company_name = ad["string_map_data"]["Author"]["value"]

        # Update the results dictionary
        if company_name in results:
            results[company_name] += 1
        else:
            results[company_name] = 1

    # Write the results to a CSV file
    with open("query_responses/results.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company_name, count in results.items():
            writer.writerow([company_name, count])