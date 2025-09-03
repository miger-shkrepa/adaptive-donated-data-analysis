import os
import json
import csv

root_dir = "root_dir"

def get_company_ads_viewed(root_dir):
    """
    This function reads the ads_viewed.json file and returns a dictionary with company names as keys and the number of ads viewed as values.
    """
    company_ads_viewed = {}
    try:
        ads_viewed_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_viewed_file_path):
            return company_ads_viewed
        
        with open(ads_viewed_file_path, "r") as file:
            data = json.load(file)
            for entry in data.get("impressions_history_ads_seen", []):
                company_name = entry.get("string_map_data", {}).get("Author", {}).get("value")
                if company_name:
                    company_ads_viewed[company_name] = company_ads_viewed.get(company_name, 0) + 1
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON: {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred: {e}")
    
    return company_ads_viewed

def save_to_csv(company_ads_viewed):
    """
    This function saves the company ads viewed data to a CSV file.
    """
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads_viewed.items():
                writer.writerow([company, ads_viewed])
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred while saving to CSV: {e}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        company_ads_viewed = get_company_ads_viewed(root_dir)
        if not company_ads_viewed:
            with open("query_responses/results.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
        else:
            save_to_csv(company_ads_viewed)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred: {e}")

if __name__ == "__main__":
    main()