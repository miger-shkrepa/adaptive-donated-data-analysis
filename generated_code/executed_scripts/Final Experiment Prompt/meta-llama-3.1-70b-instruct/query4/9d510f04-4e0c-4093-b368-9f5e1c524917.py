import json
import csv
import os

root_dir = "root_dir"

def get_companies_with_access():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the JSON file
        json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            # If the file does not exist, return a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Company Name']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        # Load the JSON data
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Extract the company names
        company_names = [entry['advertiser_name'] for entry in data.get('ig_custom_audiences_all_types', [])]

        # Write the company names to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Company Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for company_name in company_names:
                writer.writerow({'Company Name': company_name})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON: {e}")
    except UnicodeEncodeError as e:
        raise ValueError(f"ValueError: Error encoding Unicode: {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred: {e}")

get_companies_with_access()