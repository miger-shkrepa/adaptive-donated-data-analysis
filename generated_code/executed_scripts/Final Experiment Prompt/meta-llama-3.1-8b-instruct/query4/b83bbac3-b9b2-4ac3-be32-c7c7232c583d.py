import csv
import json
import os

# Set the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Set the file path to the JSON file containing the advertisers
advertisers_file = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

# Check if the advertisers file exists
if not os.path.exists(advertisers_file):
    print("Warning: Advertisers file not found. Returning CSV with only column headers.")
else:
    try:
        # Load the JSON file with encoding set to 'utf-8'
        with open(advertisers_file, 'r', encoding='utf-8') as f:
            advertisers_data = json.load(f)

        # Extract the company names from the JSON data
        company_names = [advertiser["advertiser_name"] for advertiser in advertisers_data["ig_custom_audiences_all_types"]]

        # Write the company names to a CSV file with encoding set to 'utf-8'
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])  # header
            writer.writerows([[company_name] for company_name in company_names])

        print("Query results written to results.csv")

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON file: " + str(e))
    except Exception as e:
        raise ValueError("Error: An unexpected error occurred: " + str(e))