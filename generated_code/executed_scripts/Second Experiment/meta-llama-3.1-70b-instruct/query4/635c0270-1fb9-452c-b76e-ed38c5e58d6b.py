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
                if dir_name == "your_instagram_activity":
                    # Iterate over files in 'your_instagram_activity' directory
                    for file_name in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file_name)
                        if os.path.isfile(file_path) and file_name.endswith(".json"):
                            # Add company to set (assuming company name is in file name)
                            companies.add(file_name.split(".")[0])
                # Check for 'information_about_you' directory
                elif dir_name == "information_about_you":
                    # Iterate over files in 'information_about_you' directory
                    for file_name in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file_name)
                        if os.path.isfile(file_path) and file_name.endswith(".json"):
                            # Add company to set (assuming company name is in file name)
                            companies.add(file_name.split(".")[0])
                # Check for 'personal_information' directory
                elif dir_name == "personal_information":
                    # Iterate over files in 'personal_information' directory
                    for file_name in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, file_name)
                        if os.path.isfile(file_path) and file_name.endswith(".json"):
                            # Add company to set (assuming company name is in file name)
                            companies.add(file_name.split(".")[0])

        # Write companies to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company in companies:
                writer.writerow({'Company Name': company})

    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: " + str(e))
    except Exception as e:
        raise ValueError("ValueError: " + str(e))

    return

get_companies_with_access(root_dir)