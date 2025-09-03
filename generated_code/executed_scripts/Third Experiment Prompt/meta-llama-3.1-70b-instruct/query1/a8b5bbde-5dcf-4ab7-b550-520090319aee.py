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

        # Define the path to the 'ads_information' directory
        ads_info_dir = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses')

        # Check if the 'ads_information' directory exists
        if os.path.exists(ads_info_dir):
            # Define the path to the 'other_categories_used_to_reach_you.json' file
            other_categories_file = os.path.join(ads_info_dir, 'other_categories_used_to_reach_you.json')

            # Check if the 'other_categories_used_to_reach_you.json' file exists
            if os.path.exists(other_categories_file):
                # Open the 'other_categories_used_to_reach_you.json' file and read its contents
                with open(other_categories_file, 'r') as file:
                    # Since the file structure is not provided, we assume it's a simple JSON file
                    # with a list of topics of interest
                    import json
                    data = json.load(file)

                    # Extract the topics of interest from the JSON data
                    for label_value in data['label_values']:
                        if 'label' in label_value and 'value' in label_value:
                            topics_of_interest.append(label_value['value'])

        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_file = 'query_responses/results.csv'

        # Create the 'query_responses' directory if it does not exist
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the topics of interest to the CSV file
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_topics_to_csv(topics_of_interest)

    except FileNotFoundError as e:
        # If the root directory does not exist, write an empty CSV file
        output_file = 'query_responses/results.csv'
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])
        print(e)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()