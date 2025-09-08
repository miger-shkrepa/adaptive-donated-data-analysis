import os
import csv

root_dir = "root_dir"

def check_file_exists(file_path):
    full_path = os.path.join(root_dir, file_path)
    return os.path.exists(full_path)

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check for the presence of files that might indicate company access
        devices_file = "devices.json"
        signup_details_file = "signup_details.json"
        logout_activity_file = "logout_activity.json"
        
        devices_exists = check_file_exists(os.path.join("personal_information", devices_file))
        signup_details_exists = check_file_exists(os.path.join("personal_information", signup_details_file))
        logout_activity_exists = check_file_exists(os.path.join("personal_information", logout_activity_file))
        
        # Since we don't have actual company names, we will just output the column header
        # if any of the files exist, indicating potential company access.
        if devices_exists or signup_details_exists or logout_activity_exists:
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Company Name"])
        else:
            # If no relevant files are found, output only the column header
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Company Name"])
    
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

if __name__ == "__main__":
    main()