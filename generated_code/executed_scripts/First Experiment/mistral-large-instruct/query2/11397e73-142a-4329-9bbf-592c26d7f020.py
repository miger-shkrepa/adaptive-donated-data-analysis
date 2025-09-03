import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the results
results = {}

# Define the path to the ads_viewed.json file
ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

# Check if the ads_viewed.json file exists
if not os.path.exists(ads_viewed_path):
    raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")

# Read the ads_viewed.json file
try:
    with open(ads_viewed_path, 'r') as file:
        ads_data = json.load(file)
except json.JSONDecodeError:
    raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON.")

# Process the ads_viewed.json file
for ad in ads_data.get("impressions_history_ads_seen", []):
    author = ad.get("string_map_data", {}).get("Author", {}).get("value", "")
    if author:
        if author in results:
            results[author] += 1
        else:
            results[author] = 1

# Define the path to save the results CSV file
output_path = "query_responses/results.csv"

# Create the query_responses directory if it does not exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Write the results to the CSV file
with open(output_path, 'w', newline='') as csvfile:
    fieldnames = ["Company Name", "Number of Ads Viewed"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for company, count in results.items():
        writer.writerow({"Company Name": company, "Number of Ads Viewed": count})

print(f"Results saved to {output_path}")