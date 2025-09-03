import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the results
results = {}

# Define the path to the ads_viewed.json file
ads_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

# Check if the ads_viewed.json file exists
if not os.path.exists(ads_viewed_file):
    raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")

# Open the ads_viewed.json file
with open(ads_viewed_file, 'r') as f:
    data = json.load(f)

# Iterate over the impressions_history_ads_seen list
for ad in data["impressions_history_ads_seen"]:
    # Get the author of the ad
    author = ad["string_map_data"]["Author"]["value"]

    # If the author is not in the results dictionary, add them
    if author not in results:
        results[author] = 0

    # Increment the number of ads viewed for the author
    results[author] += 1

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(["Company Name", "Number of Ads Viewed"])

    # Write the results
    for author, count in results.items():
        writer.writerow([author, count])