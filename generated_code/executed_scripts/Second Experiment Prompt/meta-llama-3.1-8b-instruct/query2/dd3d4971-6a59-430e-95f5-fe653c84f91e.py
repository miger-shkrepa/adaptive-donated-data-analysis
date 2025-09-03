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

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), "r") as f:
            # Load the JSON data
            data = json.load(f)

            # Check if the JSON data has the required structure
            if "ads_information" in data and "ads_and_topics" in data["ads_information"]:
                # Iterate over the ads and topics
                for topic in data["ads_information"]["ads_and_topics"].values():
                    # Check if the topic has the required structure
                    if "ads_viewed.json" in topic:
                        # Load the ads viewed data
                        ads_viewed_data = topic["ads_viewed.json"]

                        # Extract the company name and number of ads viewed
                        company_name = "Unknown"
                        num_ads_viewed = 0
                        if "impressions_history_ads_seen" in ads_viewed_data["structure"]:
                            for impression in ads_viewed_data["structure"]["impressions_history_ads_seen"]:
                                if "string_map_data" in impression:
                                    for key, value in impression["string_map_data"].items():
                                        if value["value"] == "str":
                                            company_name = key
                                            break
                                if "Author" in impression["string_map_data"]:
                                    num_ads_viewed += 1

                        # Add the result to the list
                        results.append((company_name, num_ads_viewed))

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(results)