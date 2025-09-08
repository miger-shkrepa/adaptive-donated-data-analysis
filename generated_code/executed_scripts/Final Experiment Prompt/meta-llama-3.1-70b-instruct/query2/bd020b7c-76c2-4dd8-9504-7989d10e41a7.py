import json
import os
import csv

root_dir = "root_dir"

def get_company_ads_viewed(root_dir):
    """
    This function calculates the number of ads viewed for each company.
    
    Args:
    root_dir (str): The path to the root directory containing user data.
    
    Returns:
    dict: A dictionary where the keys are company names and the values are the number of ads viewed.
    """
    
    company_ads_viewed = {}
    
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the ads_viewed.json file exists
    ads_viewed_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    if not os.path.exists(ads_viewed_file_path):
        return company_ads_viewed
    
    try:
        # Open and load the ads_viewed.json file
        with open(ads_viewed_file_path, "r") as file:
            data = json.load(file)
        
        # Iterate over each entry in impressions_history_ads_seen
        for entry in data.get("impressions_history_ads_seen", []):
            # Get the company name from the string_map_data
            company_name = entry.get("string_map_data", {}).get("Author", {}).get("value")
            
            # If the company name is not None, increment its count in the dictionary
            if company_name is not None:
                company_ads_viewed[company_name] = company_ads_viewed.get(company_name, 0) + 1
    
    except json.JSONDecodeError:
        raise ValueError("Error: The ads_viewed.json file is not a valid JSON file.")
    
    return company_ads_viewed

def save_to_csv(company_ads_viewed):
    """
    This function saves the company ads viewed data to a CSV file.
    
    Args:
    company_ads_viewed (dict): A dictionary where the keys are company names and the values are the number of ads viewed.
    """
    
    # Create the query_responses directory if it does not exist
    query_responses_dir = "query_responses"
    if not os.path.exists(query_responses_dir):
        os.makedirs(query_responses_dir)
    
    # Save the data to a CSV file
    with open(os.path.join(query_responses_dir, "results.csv"), "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        
        # If the company_ads_viewed dictionary is empty, do not write any rows
        if company_ads_viewed:
            for company, ads_viewed in company_ads_viewed.items():
                writer.writerow([company, ads_viewed])

def main():
    try:
        company_ads_viewed = get_company_ads_viewed(root_dir)
        save_to_csv(company_ads_viewed)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Save an empty CSV file with only the column headers
        with open(os.path.join("query_responses", "results.csv"), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])

if __name__ == "__main__":
    main()