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
        results = {}

        # Iterate over the subdirectories in the root directory
        for subdir in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, subdir)

            # Check if the subdirectory is 'ads_information'
            if subdir == 'ads_information':
                # Iterate over the files in the 'ads_information' subdirectory
                for filename in os.listdir(subdir_path):
                    file_path = os.path.join(subdir_path, filename)

                    # Check if the file is 'ads_viewed.json'
                    if filename == 'ads_viewed.json':
                        # Open and load the JSON file
                        with open(file_path, 'r') as file:
                            data = json.load(file)

                            # Iterate over the impressions history
                            for impression in data['impressions_history_ads_seen']:
                                # Get the company name and ad topic
                                company_name = impression['string_map_data']['Author']['value']

                                # Update the results dictionary
                                if company_name in results:
                                    results[company_name] += 1
                                else:
                                    results[company_name] = 1

        return results

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_results_to_csv(results):
    try:
        # Create the 'query_responses' directory if it does not exist
        query_responses_dir = 'query_responses'
        if not os.path.exists(query_responses_dir):
            os.makedirs(query_responses_dir)

        # Save the results to a CSV file
        with open(os.path.join(query_responses_dir, 'results.csv'), 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
            for company, count in results.items():
                writer.writerow([company, count])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        results = get_ads_viewed(root_dir)
        save_results_to_csv(results)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()