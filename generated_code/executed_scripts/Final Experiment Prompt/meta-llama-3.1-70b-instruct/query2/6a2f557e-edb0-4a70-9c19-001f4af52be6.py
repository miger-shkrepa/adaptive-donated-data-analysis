import json
import os
import csv

root_dir = "root_dir"

def get_company_ads_viewed(root_dir):
    """
    This function reads the ads_viewed.json file and returns a dictionary with company names as keys and the number of ads viewed as values.
    """
    company_ads_viewed = {}
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the ads_viewed.json file exists
    ads_viewed_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    if not os.path.exists(ads_viewed_file_path):
        return company_ads_viewed
    
    # Try to open and read the ads_viewed.json file
    try:
        with open(ads_viewed_file_path, "r") as file:
            data = json.load(file)
            for impression in data.get("impressions_history_ads_seen", []):
                company_name = impression.get("string_map_data", {}).get("Author", {}).get("value")
                if company_name:
                    company_ads_viewed[company_name] = company_ads_viewed.get(company_name, 0) + 1
    except json.JSONDecodeError:
        raise ValueError("Error: The ads_viewed.json file is not a valid JSON file.")
    
    return company_ads_viewed

def save_to_csv(company_ads_viewed):
    """
    This function saves the company ads viewed data to a CSV file.
    """
    csv_file_path = "query_responses/results.csv"
    csv_dir = os.path.dirname(csv_file_path)
    
    # Create the query_responses directory if it does not exist
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    
    # Try to open and write to the CSV file
    try:
        with open(csv_file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads_viewed.items():
                writer.writerow([company, ads_viewed])
    except Exception as e:
        raise Exception(f"Error: Failed to write to the CSV file. {str(e)}")

def main():
    try:
        company_ads_viewed = get_company_ads_viewed(root_dir)
        save_to_csv(company_ads_viewed)
    except Exception as e:
        print(f"Error: {str(e)}")
        # Save a CSV file with only the column headers if an error occurs
        csv_file_path = "query_responses/results.csv"
        csv_dir = os.path.dirname(csv_file_path)
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)
        with open(csv_file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])

if __name__ == "__main__":
    main()