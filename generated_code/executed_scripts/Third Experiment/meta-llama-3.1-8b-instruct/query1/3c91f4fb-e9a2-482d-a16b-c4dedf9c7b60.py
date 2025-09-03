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
        with open(os.path.join(root_dir, filename), 'r') as f:
            # Load the JSON data
            data = json.load(f)
            
            # Check if the JSON file contains the required structure
            if 'label_values' in data['structure']:
                # Iterate over the label values
                for label_value in data['structure']['label_values']:
                    # Check if the label value contains a 'label' key
                    if 'label' in label_value:
                        # Add the label to the topics of interest list
                        topics_of_interest.append(label_value['label'])
            
            # Check if the JSON file contains the required structure
            elif 'label' in data['structure']:
                # Iterate over the labels
                for label in data['structure']['label']:
                    # Add the label to the topics of interest list
                    topics_of_interest.append(label)

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Topics of Interest'])
    writer.writerows([topic] for topic in topics_of_interest)