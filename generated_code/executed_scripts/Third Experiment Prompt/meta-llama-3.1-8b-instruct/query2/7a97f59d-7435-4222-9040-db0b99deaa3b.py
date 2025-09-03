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

            # Check if the file is in the "ads_information" directory
            if "ads_information" in data:
                # Iterate over the files in the "ads_information" directory
                for sub_filename in data["ads_information"]:
                    # Check if the file is a JSON file
                    if sub_filename.endswith(".json"):
                        # Open the JSON file
                        with open(os.path.join(root_dir, "ads_information", sub_filename), "r") as sub_f:
                            # Load the JSON data
                            sub_data = json.load(sub_f)

                            # Check if the file has a "structure" key
                            if "structure" in sub_data:
                                # Iterate over the items in the "structure" dictionary
                                for item in sub_data["structure"]:
                                    # Check if the item has a "string_map_data" key
                                    if "string_map_data" in item:
                                        # Iterate over the items in the "string_map_data" dictionary
                                        for sub_item in item["string_map_data"]:
                                            # Check if the item has a "value" key
                                            if "value" in sub_item:
                                                # Extract the company name and number of ads viewed
                                                company_name = sub_item["value"]
                                                num_ads_viewed = 0

                                                # Check if the file has a "impressions_history_recs_hidden_authors" key
                                                if "impressions_history_recs_hidden_authors" in sub_data["structure"]:
                                                    # Iterate over the items in the "impressions_history_recs_hidden_authors" list
                                                    for author in sub_data["structure"]["impressions_history_recs_hidden_authors"]:
                                                        # Check if the author has a "string_map_data" key
                                                        if "string_map_data" in author:
                                                            # Iterate over the items in the "string_map_data" dictionary
                                                            for sub_author in author["string_map_data"]:
                                                                # Check if the item has a "value" key
                                                                if "value" in sub_author:
                                                                    # Increment the number of ads viewed
                                                                    num_ads_viewed += 1

                                                # Add the result to the list
                                                results.append([company_name, num_ads_viewed])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(results)