import os
import json
import csv

root_dir = "root_dir"

def get_companies_with_access_to_instagram_activity(root_directory):
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        companies_with_access = set()
        
        # Define paths for relevant files
        signup_details_path = os.path.join(root_directory, "personal_information", "signup_details.json")
        devices_path = os.path.join(root_directory, "devices", "devices.json")
        profile_based_in_path = os.path.join(root_directory, "information_about_you", "profile_based_in.json")
        
        # Process signup_details.json
        if os.path.exists(signup_details_path):
            with open(signup_details_path, 'r') as file:
                signup_data = json.load(file)
                for entry in signup_data.get("account_history_registration_info", []):
                    device = entry["string_map_data"].get("Device", {}).get("value")
                    if device:
                        companies_with_access.add(device)
        
        # Process devices.json
        if os.path.exists(devices_path):
            with open(devices_path, 'r') as file:
                devices_data = json.load(file)
                for entry in devices_data.get("devices_devices", []):
                    user_agent = entry["string_map_data"].get("User Agent", {}).get("value")
                    if user_agent:
                        companies_with_access.add(user_agent)
        
        # Process profile_based_in.json
        if os.path.exists(profile_based_in_path):
            with open(profile_based_in_path, 'r') as file:
                profile_data = json.load(file)
                for entry in profile_data.get("inferred_data_primary_location", []):
                    city_name = entry["string_map_data"].get("City Name", {}).get("value")
                    if city_name:
                        companies_with_access.add(city_name)
        
        # Write results to CSV
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name"])
            for company in companies_with_access:
                writer.writerow([company])
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Call the function with the root directory
try:
    get_companies_with_access_to_instagram_activity(root_dir)
except Exception as e:
    print(e)