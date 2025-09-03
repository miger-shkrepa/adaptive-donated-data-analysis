import os
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Initialize a list to store the results
results = []

# Function to parse the signup information
def parse_signup_information(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            import json
            data = json.load(file)
            for entry in data.get('account_history_registration_info', []):
                signup_time_str = entry['string_map_data'].get('Zeit', {}).get('value', "Unknown")
                if signup_time_str:
                    try:
                        signup_time = datetime.strptime(signup_time_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
                    except ValueError:
                        signup_time = "Unknown"
                else:
                    signup_time = "Unknown"
                results.append({
                    'Changed': 'Signup Information',
                    'New Value': entry['string_map_data'].get('Benutzername', {}).get('value', "Unknown"),
                    'Change Date': signup_time
                })
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The signup_information.json file does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error parsing signup_information.json - {str(e)}")

# Function to parse the account information
def parse_account_information(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            import json
            data = json.load(file)
            for entry in data.get('profile_account_insights', []):
                last_login_str = entry['string_map_data'].get('Letzte Anmeldung', {}).get('value', "Unknown")
                if last_login_str:
                    try:
                        last_login = datetime.strptime(last_login_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
                    except ValueError:
                        last_login = "Unknown"
                else:
                    last_login = "Unknown"
                results.append({
                    'Changed': 'Last Login',
                    'New Value': last_login,
                    'Change Date': last_login
                })
                last_logout_str = entry['string_map_data'].get('Letzte Abmeldung', {}).get('value', "Unknown")
                if last_logout_str:
                    try:
                        last_logout = datetime.strptime(last_logout_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
                    except ValueError:
                        last_logout = "Unknown"
                else:
                    last_logout = "Unknown"
                results.append({
                    'Changed': 'Last Logout',
                    'New Value': last_logout,
                    'Change Date': last_logout
                })
            for entry in data.get('profile_user', []):
                phone_verified = entry['string_map_data'].get('Telefonnummer bestätigt', {}).get('value', "Unknown")
                phone_verified_date = entry['string_map_data'].get('Telefonnummer bestätigt', {}).get('timestamp', 0)
                if phone_verified_date:
                    phone_verified_date = datetime.fromtimestamp(phone_verified_date / 1000).strftime('%Y-%m-%d')
                else:
                    phone_verified_date = "Unknown"
                results.append({
                    'Changed': 'Phone Verified',
                    'New Value': phone_verified,
                    'Change Date': phone_verified_date
                })
                email_verified = entry['string_map_data'].get('E-Mail-Adresse', {}).get('value', "Unknown")
                email_verified_date = entry['string_map_data'].get('E-Mail-Adresse', {}).get('timestamp', 0)
                if email_verified_date:
                    email_verified_date = datetime.fromtimestamp(email_verified_date / 1000).strftime('%Y-%m-%d')
                else:
                    email_verified_date = "Unknown"
                results.append({
                    'Changed': 'Email Verified',
                    'New Value': email_verified,
                    'Change Date': email_verified_date
                })
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The account_information.json file does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error parsing account_information.json - {str(e)}")

# Main function to execute the parsing
def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the paths to the JSON files
        signup_info_path = os.path.join(root_dir, 'security_and_login_information', 'login_and_account_creation', 'signup_information.json')
        account_info_path = os.path.join(root_dir, 'personal_information', 'personal_information', 'personal_information.json')
        
        # Parse the signup information
        if os.path.exists(signup_info_path):
            parse_signup_information(signup_info_path)
        else:
            print("Warning: signup_information.json does not exist. Skipping this file.")
        
        # Parse the account information
        if os.path.exists(account_info_path):
            parse_account_information(account_info_path)
        else:
            print("Warning: account_information.json does not exist. Skipping this file.")
        
        # Write the results to the CSV file
        if not os.path.exists(os.path.dirname(output_csv_path)):
            os.makedirs(os.path.dirname(output_csv_path))
        
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Changed', 'New Value', 'Change Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")

# Execute the main function
if __name__ == "__main__":
    main()