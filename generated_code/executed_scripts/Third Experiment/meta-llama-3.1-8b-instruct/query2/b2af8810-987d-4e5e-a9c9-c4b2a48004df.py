import csv
import os

# Define the root directory variable
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store the results
results = []

# Iterate over the ads_and_topics directory
for file in os.listdir(root_dir):
    if file.startswith("ads_and_topics"):
        # Open the JSON file
        with open(os.path.join(root_dir, file), 'r') as f:
            data = json.load(f)
            # Iterate over the ads_and_topics dictionary
            for key, value in data.items():
                # Check if the file is a JSON file
                if value['type'] == 'json':
                    # Initialize the count of ads viewed
                    ads_viewed = 0
                    # Initialize the list of company names
                    company_names = []
                    # Iterate over the impressions_history_ads_seen list
                    for item in value['structure']['impressions_history_ads_seen']:
                        # Increment the count of ads viewed
                        ads_viewed += 1
                        # Get the company name from the string_map_data dictionary
                        company_name = item['string_map_data']['Author']['value']
                        # Add the company name to the list
                        company_names.append(company_name)
                    # Append the result to the list
                    results.append([company_name, ads_viewed])

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(results)