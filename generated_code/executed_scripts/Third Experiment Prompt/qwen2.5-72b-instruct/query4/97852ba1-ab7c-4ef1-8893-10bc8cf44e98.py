import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def get_companies_with_access(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the relevant JSON file
        json_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            print("Warning: The required JSON file does not exist. Returning an empty CSV file.")
            return []

        # Read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Extract the list of companies
        companies = []
        for entry in data.get("ig_custom_audiences_all_types", []):
            companies.append(entry.get("advertiser_name", ""))

        return companies

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(companies):
    # Define the output CSV file path
    output_file = 'query_responses/results.csv'

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Write the companies to the CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])  # Write the header
        for company in companies:
            writer.writerow([company])

# Main execution
if __name__ == "__main__":
    try:
        companies = get_companies_with_access(root_dir)
        write_to_csv(companies)
        print(f"CSV file has been created at {os.path.abspath('query_responses/results.csv')}")
    except Exception as e:
        print(e)