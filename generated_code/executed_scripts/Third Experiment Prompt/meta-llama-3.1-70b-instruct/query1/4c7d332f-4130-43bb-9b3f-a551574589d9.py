import os
import csv
import json

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize topics of interest
        topics_of_interest = []

        # Define the path to the 'ads_information' directory
        ads_information_dir = os.path.join(root_dir, 'ads_information')

        # Check if the 'ads_information' directory exists
        if os.path.exists(ads_information_dir):
            # Define the path to the 'instagram_ads_and_businesses' directory
            instagram_ads_and_businesses_dir = os.path.join(ads_information_dir, 'instagram_ads_and_businesses')

            # Check if the 'instagram_ads_and_businesses' directory exists
            if os.path.exists(instagram_ads_and_businesses_dir):
                # Define the path to the 'subscription_for_no_ads.json' file
                subscription_for_no_ads_file = os.path.join(instagram_ads_and_businesses_dir, 'subscription_for_no_ads.json')

                # Check if the 'subscription_for_no_ads.json' file exists
                if os.path.exists(subscription_for_no_ads_file):
                    # Open and read the 'subscription_for_no_ads.json' file
                    with open(subscription_for_no_ads_file, 'r') as file:
                        data = json.load(file)

                        # Check if the 'label_values' key exists in the data
                        if 'label_values' in data:
                            # Extract the topics of interest from the 'label_values' list
                            for label_value in data['label_values']:
                                # Check if the 'label' key exists in the label_value dictionary
                                if 'label' in label_value:
                                    topics_of_interest.append(label_value['label'])

        # Return the topics of interest
        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_csv_file = 'query_responses/results.csv'

        # Create the 'query_responses' directory if it does not exist
        output_dir = os.path.dirname(output_csv_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open and write to the output CSV file
        with open(output_csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])  # Write the header

            # Write the topics of interest to the CSV file
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)

        # If no topics of interest are found, save a CSV file with only the header
        if not topics_of_interest:
            save_topics_to_csv([])
        else:
            save_topics_to_csv(topics_of_interest)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()