import os
import json
import csv

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the results
        ads_viewed = {}

        # Iterate over the subdirectories in the root directory
        for subdir in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, subdir)

            # Check if the subdirectory is 'ads_information'
            if subdir == 'ads_information':
                # Iterate over the files in the 'ads_information' subdirectory
                for filename in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, filename)

                    # Check if the file is 'ads_and_topics'
                    if filename == 'ads_and_topics':
                        # Iterate over the files in the 'ads_and_topics' subdirectory
                        for topic_filename in os.listdir(file_path):
                            topic_file_path = os.path.join(file_path, topic_filename)

                            # Check if the file is a JSON file
                            if topic_filename.endswith('.json'):
                                # Open the JSON file and load its data
                                with open(topic_file_path, 'r') as f:
                                    data = json.load(f)

                                    # Get the company name and the number of ads viewed
                                    company_name = topic_filename.replace('.json', '')
                                    num_ads_viewed = len(data.get('impressions_history_ads_seen', []))

                                    # Update the results dictionary
                                    ads_viewed[company_name] = num_ads_viewed

        return ads_viewed

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(ads_viewed):
    try:
        # Create the 'query_responses' directory if it does not exist
        query_responses_dir = 'query_responses'
        if not os.path.exists(query_responses_dir):
            os.makedirs(query_responses_dir)

        # Save the results to a CSV file
        with open(os.path.join(query_responses_dir, 'results.csv'), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
            for company, num_ads in ads_viewed.items():
                writer.writerow([company, num_ads])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        save_to_csv(ads_viewed)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()