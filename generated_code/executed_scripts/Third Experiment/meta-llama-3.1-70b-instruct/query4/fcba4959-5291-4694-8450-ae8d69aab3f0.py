import os
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate over all files and directories in the root directory
        for dir_name in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, dir_name)
            if os.path.isdir(dir_path):
                # Check if 'your_instagram_activity' directory exists
                if dir_name == 'your_instagram_activity':
                    # Iterate over all files and directories in 'your_instagram_activity'
                    for activity_dir_name in os.listdir(dir_path):
                        activity_dir_path = os.path.join(dir_path, activity_dir_name)
                        if os.path.isdir(activity_dir_path):
                            # Check if 'avatars_store', 'comments', 'events', 'likes', 'information_about_you', 'personal_information' directories exist
                            if activity_dir_name in ['avatars_store', 'comments', 'events', 'likes', 'information_about_you', 'personal_information']:
                                # Iterate over all files in the current directory
                                for file_name in os.listdir(activity_dir_path):
                                    file_path = os.path.join(activity_dir_path, file_name)
                                    if os.path.isfile(file_path) and file_name.endswith('.json'):
                                        # Add company to the set (for simplicity, assume the company name is the file name without extension)
                                        companies.add(file_name.split('.')[0])
                        elif os.path.isfile(activity_dir_path) and activity_dir_name.endswith('.json'):
                            # Add company to the set (for simplicity, assume the company name is the file name without extension)
                            companies.add(activity_dir_name.split('.')[0])

        # Write companies to CSV file
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