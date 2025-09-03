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
    
    # Iterate over the JSON files in the directory
    for filename in os.listdir(root_dir):
        if filename.endswith(".json"):
            # Open the JSON file and load its contents
            with open(os.path.join(root_dir, filename), 'r') as f:
                data = json.load(f)
                
                # Check if the JSON file contains the 'information_about_you' key
                if 'information_about_you' in data:
                    # Iterate over the JSON files in the 'information_about_you' key
                    for sub_filename in os.listdir(os.path.join(root_dir, filename)):
                        if sub_filename.endswith(".json"):
                            # Open the JSON file and load its contents
                            with open(os.path.join(root_dir, filename, sub_filename), 'r') as sub_f:
                                sub_data = json.load(sub_f)
                                
                                # Check if the JSON file contains the 'locations_of_interest.json' key
                                if 'locations_of_interest.json' in sub_data:
                                    # Iterate over the JSON files in the 'locations_of_interest.json' key
                                    for loc_filename in os.listdir(os.path.join(root_dir, filename, sub_filename)):
                                        if loc_filename.endswith(".json"):
                                            # Open the JSON file and load its contents
                                            with open(os.path.join(root_dir, filename, sub_filename, loc_filename), 'r') as loc_f:
                                                loc_data = json.load(loc_f)
                                                
                                                # Extract the topics of interest from the JSON file
                                                topics_of_interest.extend([label['label'] for label in loc_data['label_values']])
    
    # Write the topics of interest to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
        writer.writerows([[topic] for topic in topics_of_interest])
    
except FileNotFoundError as e:
    raise e
except Exception as e:
    raise ValueError("ValueError: An error occurred while processing the data.")