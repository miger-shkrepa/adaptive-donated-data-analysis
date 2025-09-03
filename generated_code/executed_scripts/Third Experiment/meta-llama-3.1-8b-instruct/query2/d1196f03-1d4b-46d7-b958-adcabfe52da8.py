import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize lists to store the data
company_names = []
ads_viewed = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if 'ads_information' in data and 'ads_and_topics' in data['ads_information']:
                # Iterate over the ads and topics
                for ad, topic in data['ads_information']['ads_and_topics'].items():
                    # Check if the ad has the required information
                    if 'impressions_history_ads_seen' in topic['structure']:
                        # Iterate over the impressions history
                        for impression in topic['structure']['impressions_history_ads_seen']:
                            # Check if the impression has the required information
                            if 'string_map_data' in impression and 'Author' in impression['string_map_data'] and 'Time' in impression['string_map_data']:
                                # Extract the company name and ads viewed
                                company_name = impression['string_map_data']['Author']['value']
                                ads_viewed_count = 1

                                # Add the data to the lists
                                company_names.append(company_name)
                                ads_viewed.append(ads_viewed_count)

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(zip(company_names, ads_viewed))