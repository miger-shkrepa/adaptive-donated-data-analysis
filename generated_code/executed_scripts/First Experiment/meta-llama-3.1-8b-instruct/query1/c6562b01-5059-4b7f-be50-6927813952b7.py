import os
import csv
import json

# Declare the variable referring to the file input
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Initialize an empty list to store the topics of interest
    topics_of_interest = []
    
    # Iterate over the files in the root directory
    for filename in os.listdir(root_dir):
        # Check if the file is a JSON file
        if filename.endswith(".json"):
            # Open the JSON file and load its contents
            with open(os.path.join(root_dir, filename), 'r') as f:
                data = json.load(f)
                
                # Check if the JSON file contains the 'information_about_you' key
                if 'information_about_you' in data:
                    # Iterate over the JSON files in the 'information_about_you' key
                    for json_file in data['information_about_you'].values():
                        # Check if the JSON file contains the 'locations_of_interest.json' key
                        if 'locations_of_interest.json' in json_file:
                            # Open the JSON file and load its contents
                            with open(os.path.join(root_dir, json_file['locations_of_interest.json']), 'r') as f:
                                locations_data = json.load(f)
                                
                                # Iterate over the 'label_values' list in the JSON file
                                for label_value in locations_data['label_values']:
                                    # Extract the 'label' value from the dictionary
                                    topic = label_value['label']
                                    
                                    # Add the topic to the list of topics of interest
                                    topics_of_interest.append(topic)
    
    # Write the topics of interest to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
        writer.writerows([[topic] for topic in topics_of_interest])
    
except FileNotFoundError as e:
    raise e
except ValueError as e:
    raise ValueError("ValueError: The JSON file is not valid.")
except Exception as e:
    raise Exception("Error: An unexpected error occurred.")