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
    
    # Open and read the JSON file
    try:
        with open(profile_changes_path, 'r', encoding='utf-8') as file:
            import json
            data = json.load(file)
            
            # Extract the profile changes
            for change in data.get("profile_profile_change", []):
                string_map_data = change.get("string_map_data", {})
                change_date = string_map_data.get("Change Date", {}).get("value", "")
                changed = string_map_data.get("Changed", {}).get("value", "")
                new_value = string_map_data.get("New Value", {}).get("value", "")
                
                # Convert the timestamp to a readable date format
                if change_date:
                    try:
                        change_date = datetime.fromtimestamp(int(change_date)).strftime('%Y-%m-%d')
                    except ValueError:
                        change_date = ""
                
                # Append the change to the list
                changes.append((changed, new_value, change_date))
    
    except (FileNotFoundError, ValueError) as e:
        raise FileNotFoundError(f"FileNotFoundError: The file {profile_changes_path} does not exist or is not a valid JSON file.") from e
    
    return changes

def save_to_csv(changes, output_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the changes to a CSV file
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Changed", "New Value", "Change Date"])
        csvwriter.writerows(changes)

def main():
    try:
        # Get the profile changes
        changes = get_profile_changes(root_dir)
        
        # Define the output path
        output_path = "query_responses/results.csv"
        
        # Save the changes to a CSV file
        save_to_csv(changes, output_path)
        
        print(f"Results saved to {output_path}")
    
    except FileNotFoundError as e:
        print(e)
        # Save an empty CSV file with headers if the file is not found
        save_to_csv([], "query_responses/results.csv")

if __name__ == "__main__":
    main()