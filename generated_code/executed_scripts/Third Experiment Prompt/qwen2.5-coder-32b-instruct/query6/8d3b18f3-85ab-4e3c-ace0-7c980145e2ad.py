import os
import csv
from datetime import datetime

# Variable referring to the file input
root_dir = "root_dir"

def get_profile_changes(root_dir):
    # Define the path to the profile_changes.json file
    profile_changes_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")
    
    # Check if the file exists
    if not os.path.exists(profile_changes_path):
        # Return an empty list if the file does not exist
        return []
    
    # Initialize a list to store the changes
    changes = []
    
    try:
        # Open and read the JSON file
        with open(profile_changes_path, 'r', encoding='utf-8') as file:
            import json
            data = json.load(file)
            
            # Check if the expected structure exists
            if 'profile_profile_change' in data:
                for change in data['profile_profile_change']:
                    if 'string_map_data' in change:
                        string_map_data = change['string_map_data']
                        changed = string_map_data.get('Changed', {}).get('value', '')
                        new_value = string_map_data.get('New Value', {}).get('value', '')
                        change_date_timestamp = string_map_data.get('Change Date', {}).get('timestamp', 0)
                        
                        # Convert timestamp to a readable date format
                        change_date = datetime.fromtimestamp(change_date_timestamp / 1000).strftime('%Y-%m-%d')
                        
                        # Append the change to the list
                        changes.append((changed, new_value, change_date))
    
    except Exception as e:
        # Raise a ValueError with a structured error message
        raise ValueError(f"ValueError: Error reading or parsing the profile_changes.json file - {str(e)}")
    
    return changes

def save_changes_to_csv(changes, output_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Open the CSV file for writing
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write the header
            writer.writerow(["Changed", "New Value", "Change Date"])
            
            # Write the data rows
            for change in changes:
                writer.writerow(change)
    
    except Exception as e:
        # Raise a ValueError with a structured error message
        raise ValueError(f"ValueError: Error writing to the CSV file - {str(e)}")

def main():
    try:
        # Get the profile changes
        changes = get_profile_changes(root_dir)
        
        # Define the output path
        output_path = 'query_responses/results.csv'
        
        # Save the changes to a CSV file
        save_changes_to_csv(changes, output_path)
        
        print(f"Results saved to {output_path}")
    
    except FileNotFoundError as e:
        # Handle FileNotFoundError
        print(e)
    except ValueError as e:
        # Handle ValueError
        print(e)

if __name__ == "__main__":
    main()