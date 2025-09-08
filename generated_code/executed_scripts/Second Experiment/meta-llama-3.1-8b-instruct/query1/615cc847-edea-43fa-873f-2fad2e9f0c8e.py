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
            data = file.read()
            # Parse the JSON data
            import json
            parsed_data = json.loads(data)
            # Check if the JSON data contains the 'information_about_you' key
            if 'information_about_you' in parsed_data:
                # Check if the JSON data contains the 'locations_of_interest.json' key
                if 'locations_of_interest.json' in parsed_data['information_about_you']:
                    # Open the 'locations_of_interest.json' file
                    with open(os.path.join(root_dir, 'information_about_you', 'locations_of_interest.json'), 'r') as locations_file:
                        # Load the JSON data
                        locations_data = locations_file.read()
                        # Parse the JSON data
                        locations_parsed_data = json.loads(locations_data)
                        # Check if the JSON data contains the 'label_values' key
                        if 'label_values' in locations_parsed_data:
                            # Iterate over the label values
                            for label_value in locations_parsed_data['label_values']:
                                # Check if the label value contains the 'label' key
                                if 'label' in label_value:
                                    # Append the label to the topics of interest list
                                    topics_of_interest.append(label_value['label'])

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Topics of Interest'])
    # Write the topics of interest
    writer.writerow(topics_of_interest)