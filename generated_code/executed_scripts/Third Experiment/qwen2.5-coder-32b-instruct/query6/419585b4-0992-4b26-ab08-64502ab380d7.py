import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

# Function to check if the directory exists
def check_directory_exists(directory):
    if not os.path.exists(directory):
        raise FileNotFoundError(f"FileNotFoundError: The root directory {directory} does not exist.")

# Function to check if the file exists
def check_file_exists(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")

# Main function to process the data
def process_account_changes(root_dir):
    try:
        # Check if the root directory exists
        check_directory_exists(root_dir)
        
        # Define the path to the account history file
        account_history_path = os.path.join(root_dir, "account_history_registration_info.json")
        
        # Check if the account history file exists
        check_file_exists(account_history_path)
        
        # Initialize the list to store the changes
        changes = []
        
        # Open and read the account history file
        with open(account_history_path, 'r') as file:
            import json
            account_data = json.load(file)
            
            # Process each entry in the account history
            for entry in account_data.get("account_history_registration_info", []):
                string_map_data = entry.get("string_map_data", {})
                
                # Extract relevant information
                for key, data in string_map_data.items():
                    if key in ["Benutzername", "E-Mail-Adresse", "Telefonnummer"]:
                        changes.append({
                            "Changed": key,
                            "New Value": data.get("value", ""),
                            "Change Date": datetime.fromtimestamp(data.get("timestamp", 0)).strftime('%Y-%m-%d')
                        })
        
        # Define the path to save the CSV file
        csv_file_path = "query_responses/results.csv"
        
        # Ensure the directory for the CSV file exists
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        
        # Write the changes to the CSV file
        with open(csv_file_path, mode='w', newline='') as csv_file:
            fieldnames = ["Changed", "New Value", "Change Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(changes)
    
    except FileNotFoundError as e:
        # Create a CSV file with only the column headers if the required file is not found
        csv_file_path = "query_responses/results.csv"
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        
        with open(csv_file_path, mode='w', newline='') as csv_file:
            fieldnames = ["Changed", "New Value", "Change Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

# Call the main function
process_account_changes(root_dir)