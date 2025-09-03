import os
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty list to store topics of interest
        topics_of_interest = []

        # Check if the 'ads_information' directory exists
        ads_info_dir = os.path.join(root_dir, 'ads_information')
        if os.path.exists(ads_info_dir):
            # Check if the 'other_categories_used_to_reach_you.json' file exists
            other_categories_file = os.path.join(ads_info_dir, 'instagram_ads_and_businesses', 'other_categories_used_to_reach_you.json')
            if os.path.exists(other_categories_file):
                # Open and read the 'other_categories_used_to_reach_you.json' file
                with open(other_categories_file, 'r') as file:
                    # Since we don't have the actual JSON data, we'll assume it's in the correct format
                    # and extract the 'label' values from the 'label_values' list
                    # For simplicity, let's assume the JSON data is a dictionary with a single key 'label_values'
                    # and the value is a list of dictionaries with a 'label' key
                    import json
                    data = json.load(file)
                    topics_of_interest = [label['label'] for label in data['label_values']]

        # If no topics of interest are found, return an empty list
        if not topics_of_interest:
            raise ValueError("ValueError: No topics of interest found.")

        return topics_of_interest

    except Exception as e:
        # Raise a FileNotFoundError or ValueError with a custom error message
        if isinstance(e, FileNotFoundError):
            raise FileNotFoundError("FileNotFoundError: " + str(e))
        elif isinstance(e, ValueError):
            raise ValueError("ValueError: " + str(e))
        else:
            raise Exception("Error: " + str(e))

def write_to_csv(topics_of_interest):
    try:
        # Create the 'query_responses' directory if it doesn't exist
        query_responses_dir = 'query_responses'
        if not os.path.exists(query_responses_dir):
            os.makedirs(query_responses_dir)

        # Write the topics of interest to a CSV file
        with open(os.path.join(query_responses_dir, 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise Exception("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest)
    except Exception as e:
        # If an error occurs, write an empty CSV file with only the column header
        with open(os.path.join('query_responses', 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
        print("Error: " + str(e))

if __name__ == "__main__":
    main()