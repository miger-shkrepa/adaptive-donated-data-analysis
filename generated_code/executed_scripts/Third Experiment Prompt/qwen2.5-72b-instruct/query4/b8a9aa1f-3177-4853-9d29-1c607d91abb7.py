import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        companies = set()

        # Path to the specific JSON file
        json_file_path = os.path.join(root_dir, 'apps_and_websites_off_of_instagram', 'apps_and_websites', 'your_activity_off_meta_technologies.json')

        if not os.path.exists(json_file_path):
            return companies

        with open(json_file_path, 'r') as file:
            data = json.load(file)

            if 'apps_and_websites_off_meta_activity' in data:
                for entry in data['apps_and_websites_off_meta_activity']:
                    if 'name' in entry:
                        companies.add(entry['name'])

        return companies

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(companies, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to CSV - {e}")

if __name__ == "__main__":
    try:
        companies_with_access = get_companies_with_access(root_dir)
        write_to_csv(companies_with_access, 'query_responses/results.csv')
    except Exception as e:
        print(e)