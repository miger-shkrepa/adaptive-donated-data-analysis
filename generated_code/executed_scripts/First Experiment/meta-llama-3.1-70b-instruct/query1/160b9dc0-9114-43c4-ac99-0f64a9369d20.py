import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
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
                # Check if the directory is 'information_about_you'
                if filename == 'information_about_you':
                    # Iterate over all files in the 'information_about_you' directory
                    for info_filename in os.listdir(os.path.join(root_dir, filename)):
                        # Check if the file is 'locations_of_interest.json'
                        if info_filename == 'locations_of_interest.json':
                            # Open the 'locations_of_interest.json' file
                            with open(os.path.join(root_dir, filename, info_filename), 'r') as file:
                                # Load the JSON data
                                data = json.load(file)
                                # Iterate over the 'label_values' list
                                for label_value in data['label_values']:
                                    # Check if the label_value is a dictionary with a 'label' key
                                    if isinstance(label_value, dict) and 'label' in label_value:
                                        # Append the label to the topics_of_interest list
                                        topics_of_interest.append(label_value['label'])
                                    # Check if the label_value is a dictionary with a 'value' key
                                    elif isinstance(label_value, dict) and 'value' in label_value:
                                        # Append the value to the topics_of_interest list
                                        topics_of_interest.append(label_value['value'])

        # Return the topics_of_interest list
        return topics_of_interest

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

def save_to_csv(topics_of_interest):
    try:
        # Open the 'results.csv' file in write mode
        with open('query_responses/results.csv', 'w', newline='') as file:
            # Create a CSV writer
            writer = csv.writer(file)
            # Write the header
            writer.writerow(['Topics of Interest'])
            # Write each topic of interest
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the topics of interest
        topics_of_interest = get_topics_of_interest(root_dir)
        # Save the topics of interest to a CSV file
        save_to_csv(topics_of_interest)

    except Exception as e:
        # Print the error message
        print("Error: " + str(e))

if __name__ == "__main__":
    main()