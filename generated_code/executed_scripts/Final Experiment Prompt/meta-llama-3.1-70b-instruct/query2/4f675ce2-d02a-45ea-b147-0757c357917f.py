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
    
    # Read the ads_viewed.json file
    try:
        with open(ads_viewed_file_path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Error: The ads_viewed.json file is not a valid JSON file.")
    
    # Check if the impressions_history_ads_seen key exists in the data
    if "impressions_history_ads_seen" not in data:
        return company_ads_viewed
    
    # Iterate over the impressions_history_ads_seen list
    for ad in data["impressions_history_ads_seen"]:
        # Check if the string_map_data key exists in the ad
        if "string_map_data" not in ad:
            continue
        
        # Check if the Author key exists in the string_map_data
        if "Author" not in ad["string_map_data"]:
            continue
        
        # Get the company name
        company_name = ad["string_map_data"]["Author"]["value"]
        
        # Increment the number of ads viewed for the company
        if company_name in company_ads_viewed:
            company_ads_viewed[company_name] += 1
        else:
            company_ads_viewed[company_name] = 1
    
    return company_ads_viewed

def save_to_csv(company_ads_viewed):
    """
    This function saves the company ads viewed data to a CSV file.
    """
    # Create the query_responses directory if it does not exist
    query_responses_dir = "query_responses"
    if not os.path.exists(query_responses_dir):
        os.makedirs(query_responses_dir)
    
    # Save the data to a CSV file
    with open(os.path.join(query_responses_dir, "results.csv"), "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, ads_viewed in company_ads_viewed.items():
            writer.writerow([company, ads_viewed])

def main():
    try:
        company_ads_viewed = get_company_ads_viewed(root_dir)
        save_to_csv(company_ads_viewed)
    except Exception as e:
        print(f"An error occurred: {e}")
        # Save an empty CSV file with column headers if an error occurs
        with open(os.path.join("query_responses", "results.csv"), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])

if __name__ == "__main__":
    main()