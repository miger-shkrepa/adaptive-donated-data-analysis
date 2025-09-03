import os
import json
import csv

root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Initialize an empty list to store topics of interest
    topics_of_interest = []

    # Iterate over all files in the root directory
    for filename in os.listdir(root_dir):
        # Check if the file is a directory
        if os.path.isdir(os.path.join(root_dir, filename)):
            # Iterate over all files in the subdirectory
            for subfilename in os.listdir(os.path.join(root_dir, filename)):
                # Check if the file is 'locations_of_interest.json'
                if subfilename == 'locations_of_interest.json':
                    # Open the JSON file
                    with open(os.path.join(root_dir, filename, subfilename), 'r') as file:
                        # Load the JSON data
                        data = json.load(file)
                        # Extract topics of interest
                        for label_value in data['label_values']:
                            if 'vec' in label_value:
                                for value in label_value['vec']:
                                    topics_of_interest.append(value['value'])
                            else:
                                topics_of_interest.append(label_value['value'])

    # Remove duplicates from the list
    topics_of_interest = list(set(topics_of_interest))

    # Save the topics of interest to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

except FileNotFoundError as e:
    raise FileNotFoundError(f"FileNotFoundError: {e}")
except json.JSONDecodeError as e:
    raise ValueError(f"ValueError: Error parsing JSON - {e}")
except Exception as e:
    raise ValueError(f"ValueError: An error occurred - {e}")