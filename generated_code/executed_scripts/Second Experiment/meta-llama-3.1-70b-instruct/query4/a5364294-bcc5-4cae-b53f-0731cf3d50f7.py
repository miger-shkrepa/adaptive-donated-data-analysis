import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        ads_information_dir = os.path.join(root_dir, "ads_information")
        if not os.path.exists(ads_information_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_information directory does not exist.")
        
        instagram_ads_and_businesses_dir = os.path.join(ads_information_dir, "instagram_ads_and_businesses")
        if not os.path.exists(instagram_ads_and_businesses_dir):
            raise FileNotFoundError("FileNotFoundError: The instagram_ads_and_businesses directory does not exist.")
        
        advertisers_using_your_activity_or_information_file = os.path.join(instagram_ads_and_businesses_dir, "advertisers_using_your_activity_or_information.json")
        if not os.path.exists(advertisers_using_your_activity_or_information_file):
            return companies
        
        with open(advertisers_using_your_activity_or_information_file, 'r') as file:
            data = json.load(file)
            for advertiser in data["ig_custom_audiences_all_types"]:
                companies.add(advertiser["advertiser_name"])
        
        return companies
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON - {e}")
    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

def write_companies_to_csv(companies):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    
    except Exception as e:
        raise ValueError(f"ValueError: Error writing to CSV - {e}")

def main():
    try:
        companies = get_companies_with_access(root_dir)
        if not companies:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name"])
        else:
            write_companies_to_csv(companies)
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except ValueError as e:
        raise ValueError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: An error occurred - {e}")

if __name__ == "__main__":
    main()