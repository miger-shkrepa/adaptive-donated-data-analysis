import os
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate over subdirectories
        for dir_name in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, dir_name)
            if os.path.isdir(dir_path):
                # Check for 'your_instagram_activity' directory
                if dir_name == 'your_instagram_activity':
                    for file_name in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file_name)
                        if os.path.isfile(file_path) and file_name.endswith('.json'):
                            # Add company names from json files
                            companies.add(file_name.split('.')[0])
                # Check for 'information_about_you' directory
                elif dir_name == 'information_about_you':
                    for file_name in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file_name)
                        if os.path.isfile(file_path) and file_name.endswith('.json'):
                            # Add company names from json files
                            companies.add(file_name.split('.')[0])
                # Check for 'personal_information' directory
                elif dir_name == 'personal_information':
                    for file_name in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file_name)
                        if os.path.isfile(file_path) and file_name.endswith('.json'):
                            # Add company names from json files
                            companies.add(file_name.split('.')[0])

        # Create CSV file with company names
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company in companies:
                writer.writerow({'Company Name': company})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_companies_with_access(root_dir)