import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the JSON file containing topics of interest
topics_of_interest_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "other_categories_used_to_reach_you.json")

# Initialize a list to store topics of interest
topics_of_interest = []

# Check if the file exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
if not os.path.exists(topics_of_interest_file_path):
    # If the file does not exist, create an empty CSV with the header
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
    print("CSV file created with only the column headers as the required file does not exist.")
else:
    try:
        # Open and read the JSON file
        with open(topics_of_interest_file_path, 'r') as file:
            data = json.load(file)
        
        # Extract topics of interest
        if 'label_values' in data:
            for label_value in data['label_values']:
                if 'label' in label_value:
                    topics_of_interest.append(label_value['label'])
        
        # Write the topics of interest to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])
        
        print("CSV file created with topics of interest.")
    
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")