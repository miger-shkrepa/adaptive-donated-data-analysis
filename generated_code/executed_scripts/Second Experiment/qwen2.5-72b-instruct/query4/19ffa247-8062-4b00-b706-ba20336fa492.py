import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_instagram_activity(root_directory):
    companies = set()
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the paths for the relevant JSON files
        signup_details_path = os.path.join(root_directory, "personal_information", "signup_details.json")
        profile_based_in_path = os.path.join(root_directory, "information_about_you", "profile_based_in.json")
        devices_path = os.path.join(root_directory, "devices", "devices.json")
        
        # Process signup_details.json
        if os.path.exists(signup_details_path):
            with open(signup_details_path, 'r') as file:
                signup_data = json.load(file)
                for entry in signup_data.get("account_history_registration_info", []):
                    email = entry["string_map_data"].get("Email", {}).get("value")
                    if email:
                        companies.add(email.split('@')[1])
        
        # Process profile_based_in.json
        if os.path.exists(profile_based_in_path):
            with open(profile_based_in_path, 'r') as file:
                profile_data = json.load(file)
                for entry in profile_data.get("inferred_data_primary_location", []):
                    city_name = entry["string_map_data"].get("City Name", {}).get("value")
                    if city_name:
                        companies.add(city_name)
        
        # Process devices.json
        if os.path.exists(devices_path):
            with open(devices_path, 'r') as file:
                devices_data = json.load(file)
                for entry in devices_data.get("devices_devices", []):
                    user_agent = entry["string_map_data"].get("User Agent", {}).get("value")
                    if user_agent:
                        companies.add(user_agent)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")
    
    return companies

def write_companies_to_csv(companies, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
    except Exception as e:
        raise Exception(f"Error: Failed to write CSV file - {e}")

if __name__ == "__main__":
    try:
        companies_with_access = get_companies_with_access_to_instagram_activity(root_dir)
        write_companies_to_csv(companies_with_access, 'query_responses/results.csv')
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)