import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the directory structure
for dir_path, dir_names, file_names in os.walk(root_dir):
    # Check if the current directory is 'your_instagram_activity'
    if dir_names == ['your_instagram_activity']:
        # Iterate over the files in the 'your_instagram_activity' directory
        for file_name in file_names:
            # Check if the file is 'avatars_store' or 'monetization'
            if file_name in ['avatars_store', 'monetization']:
                # Add the company name to the list
                company_names.append('Instagram')

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name'])
    writer.writerows([[company] for company in company_names])