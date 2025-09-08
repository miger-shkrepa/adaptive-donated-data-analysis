import csv
import os
import json

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Set the input file path
input_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Check if the input file exists
if not os.path.exists(input_file_path):
    print("Warning: The input file does not exist. Returning CSV file with only column headers.")
else:
    try:
        # Load the JSON data
        with open(input_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract the company names
        company_names = [entry['advertiser_name'] for entry in data['ig_custom_audiences_all_types'] if 'advertiser_name' in entry]

        # Write the company names to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])  # Write the column header
            writer.writerows([[company_name] for company_name in company_names])  # Write the company names

        print("Query response saved to query_responses/results.csv")
    except json.JSONDecodeError as e:
        raise ValueError("ValueError: Failed to parse JSON data: " + str(e))
    except KeyError as e:
        raise ValueError("ValueError: Missing key in JSON data: " + str(e))