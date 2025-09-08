import csv
import os

# Declare the variable referring to the file input
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

            # Check if the JSON data contains the required structure
            if 'ads_information' in data and 'instagram_ads_and_businesses' in data['ads_information']:
                # Iterate over the label values in the JSON data
                for label_value in data['ads_information']['instagram_ads_and_businesses']['label_values']:
                    # Extract the label and value from the label value
                    label = label_value['label']
                    value = label_value['value']

                    # Add the label to the topics of interest list
                    topics_of_interest.append(label)

# Create a CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)

    # Write the column headers
    writer.writerow(['Topics of Interest'])

    # Write the topics of interest to the CSV file
    for topic in topics_of_interest:
        writer.writerow([topic])