import csv
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
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()

            # Check if the JSON data contains the required information
            if "ads_viewed.json" in data:
                # Extract the company name and number of ads viewed
                company_name = filename.split('.')[0]
                num_ads_viewed = 0

                # Check if the JSON data contains the required information
                if "impressions_history_ads_seen" in data:
                    # Extract the number of ads viewed
                    num_ads_viewed = len(data[data.find("impressions_history_ads_seen"):].split('}')[0].split('[')[1].split('}')[0].split(','))

                # Append the result to the list
                results.append([company_name, num_ads_viewed])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(results)