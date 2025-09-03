import os
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

directories_to_check = ["your_instagram_activity", "personal_information"]
companies = []

for directory in directories_to_check:
    dir_path = os.path.join(root_dir, directory)
    if os.path.exists(dir_path):
        for filename in os.listdir(dir_path):
            if filename.endswith('.json'):
                file_path = os.path.join(dir_path, filename)
                with open(file_path, 'r') as file:
                    data = file.read()
                    # Add your logic here to extract company names from the data
                    # For example, if the company name is always present in a specific key, you can use:
                    # company = data.get('company_name', 'Unknown')
                    # companies.append(company)

# Save the results to a CSV file
output_file = 'query_responses/results.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name"])
    for company in companies:
        writer.writerow([company])