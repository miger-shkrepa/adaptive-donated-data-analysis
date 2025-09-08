import json
import csv
import os

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    """
    Retrieves the list of companies that have access to your Instagram activity or information.

    Args:
        root_dir (str): The path to the root directory containing the user data.

    Returns:
        list: A list of company names that have access to your Instagram activity or information.
    """
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Construct the path to the required file
        file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

        # Check if the required file exists
        if not os.path.exists(file_path):
            # If the file does not exist, return an empty list
            return []

        # Open and load the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract the company names from the JSON data
        company_names = [entry["advertiser_name"] for entry in data.get("ig_custom_audiences_all_types", [])]

        return company_names

    except json.JSONDecodeError:
        raise ValueError("Error: Failed to parse the JSON file.")
    except KeyError:
        raise ValueError("Error: The JSON file is missing the required key.")
    except Exception as e:
        raise ValueError(f"Error: An unexpected error occurred - {str(e)}")

def save_to_csv(company_names, output_path):
    """
    Saves the list of company names to a CSV file.

    Args:
        company_names (list): The list of company names.
        output_path (str): The path to the output CSV file.
    """
    try:
        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the company names to the CSV file
        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])  # Write the header
            for company_name in company_names:
                writer.writerow([company_name])

    except Exception as e:
        raise ValueError(f"Error: Failed to save the data to the CSV file - {str(e)}")

def main():
    output_path = "query_responses/results.csv"
    company_names = get_companies_with_access(root_dir)
    save_to_csv(company_names, output_path)

if __name__ == "__main__":
    main()