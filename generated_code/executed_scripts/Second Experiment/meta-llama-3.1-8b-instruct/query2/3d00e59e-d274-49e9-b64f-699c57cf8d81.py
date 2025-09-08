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
            # Parse the JSON data
            import json
            json_data = json.loads(data)
            # Check if the JSON data contains the required information
            if 'ads_and_topics' in json_data['ads_information']:
                # Iterate over the ads and topics
                for ad, topic in json_data['ads_information']['ads_and_topics'].items():
                    # Check if the ad has a type and structure
                    if 'type' in topic and 'structure' in topic:
                        # Check if the type is 'json' and the structure has a 'impressions_history_ads_seen' key
                        if topic['type'] == 'json' and 'impressions_history_ads_seen' in topic['structure']:
                            # Initialize the count of ads viewed
                            ads_viewed = 0
                            # Iterate over the impressions history ads seen
                            for impression in topic['structure']['impressions_history_ads_seen']:
                                # Check if the impression has a string map data
                                if 'string_map_data' in impression:
                                    # Increment the count of ads viewed
                                    ads_viewed += 1
                            # Append the result to the list
                            results.append((topic['ads_viewed.json'], ads_viewed))

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Company Name', 'Number of Ads Viewed'])
    # Write the results
    for result in results:
        writer.writerow(result)