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
            data = eval(file.read())

            # Check if the JSON data contains the required information
            if 'ads_information' in data and 'ads_and_topics' in data['ads_information']:
                # Iterate over the ads and topics
                for ad, topic in data['ads_information']['ads_and_topics'].items():
                    # Check if the ad has the required information
                    if 'type' in topic and topic['type'] == 'json' and 'structure' in topic:
                        # Initialize the count of ads viewed
                        count = 0

                        # Check if the structure contains the required information
                        if 'impressions_history_ads_seen' in topic['structure']:
                            # Iterate over the impressions history ads seen
                            for impression in topic['structure']['impressions_history_ads_seen']:
                                # Check if the impression has the required information
                                if 'string_map_data' in impression:
                                    # Increment the count of ads viewed
                                    count += 1

                        # Append the result to the list
                        results.append((ad, count))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(results)