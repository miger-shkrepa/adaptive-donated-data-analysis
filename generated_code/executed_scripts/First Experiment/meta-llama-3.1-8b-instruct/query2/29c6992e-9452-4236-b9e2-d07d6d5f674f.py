import csv
import os

# Define the root directory variable
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
        # Open the JSON file and load its contents
        with open(os.path.join(root_dir, filename), 'r') as f:
            data = f.read()

        # Parse the JSON data
        import json
        json_data = json.loads(data)

        # Check if the JSON data contains the required information
        if "ads_information" in json_data and "ads_and_topics" in json_data["ads_information"]:
            # Extract the company name and number of ads viewed
            company_name = filename.split(".")[0]
            num_ads_viewed = len(json_data["ads_information"]["ads_and_topics"][company_name]["structure"]["impressions_history_ads_seen"])

            # Append the result to the list
            results.append((company_name, num_ads_viewed))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])  # header
    writer.writerows(results)