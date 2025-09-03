import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Define the path to the JSON file containing the ads information
ads_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the ads file exists
if os.path.exists(ads_file_path):
    # Open the ads file
    with open(ads_file_path, 'r') as f:
        # Load the JSON data
        data = json.load(f)

        # Iterate over the impressions history
        for impression in data["impressions_history_posts_seen"]:
            # Extract the company name and the time of the ad view
            company_name = impression["string_map_data"]["Author"]["value"]
            time = impression["string_map_data"]["Time"]["timestamp"]

            # Append the result to the list
            results.append((company_name, time))

# Sort the results by company name
results.sort(key=lambda x: x[0])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name", "Time of Ad View"])
    writer.writerows(results)