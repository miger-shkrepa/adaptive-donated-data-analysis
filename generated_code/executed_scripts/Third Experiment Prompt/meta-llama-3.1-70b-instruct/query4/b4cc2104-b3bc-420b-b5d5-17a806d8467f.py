import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access(root_dir):
    companies = set()
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Iterate through 'ads_information' directory
        ads_info_dir = os.path.join(root_dir, 'ads_information')
        if os.path.exists(ads_info_dir):
            # Iterate through 'advertising' directory
            advertising_dir = os.path.join(ads_info_dir, 'advertising')
            if os.path.exists(advertising_dir):
                # Iterate through 'advertisers' JSON files
                for filename in os.listdir(advertising_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(advertising_dir, filename)
                        with open(filepath, 'r') as file:
                            data = json.load(file)
                            # Extract company names from 'advertisers' JSON files
                            for advertiser in data.get('advertisers', []):
                                companies.add(advertiser.get('company_name', ''))

        # Iterate through 'security_and_login_information' directory
        security_dir = os.path.join(root_dir, 'security_and_login_information')
        if os.path.exists(security_dir):
            # Iterate through 'login_activity' JSON files
            login_activity_dir = os.path.join(security_dir, 'login_activity.json')
            if os.path.exists(login_activity_dir):
                with open(login_activity_dir, 'r') as file:
                    data = json.load(file)
                    # Extract company names from 'login_activity' JSON files
                    for login_activity in data.get('login_activity', []):
                        companies.add(login_activity.get('company_name', ''))

        # Write companies to CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in companies:
                writer.writerow([company])

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

get_companies_with_access(root_dir)