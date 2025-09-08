import csv
import os

# Declare the variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty dictionary to store the company names and ad counts
ad_counts = {}

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file and load its contents
        with open(os.path.join(root_dir, filename), 'r') as f:
            data = f.read()

        # Parse the JSON data
        import json
        json_data = json.loads(data)

        # Check if the JSON data contains ad information
        if "ads_information" in json_data:
            # Iterate over the ad information
            for ad_info in json_data["ads_information"]["ads_and_topics"].values():
                # Check if the ad information contains a list of ads
                if "impressions_history_ads_seen" in ad_info["structure"]:
                    # Iterate over the ads
                    for ad in ad_info["structure"]["impressions_history_ads_seen"]:
                        # Get the company name from the ad data
                        company_name = ad["string_map_data"]["Author"]["value"]

                        # Increment the ad count for the company
                        if company_name in ad_counts:
                            ad_counts[company_name] += 1
                        else:
                            ad_counts[company_name] = 1

# Create a CSV writer to write the results to a file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in ad_counts.items():
        writer.writerow([company, count])