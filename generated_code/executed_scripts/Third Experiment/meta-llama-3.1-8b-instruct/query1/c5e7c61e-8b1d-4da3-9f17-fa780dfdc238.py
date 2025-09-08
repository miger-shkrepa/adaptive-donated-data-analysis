import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the 'ads_information' key
            if 'ads_information' in data:
                # Iterate over the values in the 'ads_information' key
                for value in data['ads_information'].values():
                    # Check if the value is a dictionary
                    if isinstance(value, dict):
                        # Check if the dictionary contains the 'ads_and_topics' key
                        if 'ads_and_topics' in value:
                            # Iterate over the values in the 'ads_and_topics' key
                            for topic in value['ads_and_topics'].values():
                                # Check if the topic is a dictionary
                                if isinstance(topic, dict):
                                    # Check if the dictionary contains the 'type' key
                                    if 'type' in topic:
                                        # Check if the type is 'json'
                                        if topic['type'] == 'json':
                                            # Check if the dictionary contains the 'structure' key
                                            if 'structure' in topic:
                                                # Iterate over the values in the 'structure' key
                                                for structure in topic['structure'].values():
                                                    # Check if the structure is a dictionary
                                                    if isinstance(structure, dict):
                                                        # Check if the dictionary contains the 'impressions_history_ads_seen' key
                                                        if 'impressions_history_ads_seen' in structure:
                                                            # Iterate over the values in the 'impressions_history_ads_seen' key
                                                            for item in structure['impressions_history_ads_seen']:
                                                                # Check if the item is a dictionary
                                                                if isinstance(item, dict):
                                                                    # Check if the dictionary contains the 'string_map_data' key
                                                                    if 'string_map_data' in item:
                                                                        # Iterate over the values in the 'string_map_data' key
                                                                        for key, value in item['string_map_data'].items():
                                                                            # Check if the key is 'Topic'
                                                                            if key == 'Topic':
                                                                                # Add the topic to the list of topics of interest
                                                                                topics_of_interest.append(value['value'])

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Topics of Interest'])
    writer.writerows([[topic] for topic in topics_of_interest])

print("The script has finished running.")