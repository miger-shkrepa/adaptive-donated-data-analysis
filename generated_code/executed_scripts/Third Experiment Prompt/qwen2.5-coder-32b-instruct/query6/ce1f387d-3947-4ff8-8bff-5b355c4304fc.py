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
        with open(profile_changes_path, 'r') as file:
            import json
            data = json.load(file)
            
            # Check if the expected structure is present
            if "profile_profile_change" not in data:
                raise ValueError("ValueError: The expected structure 'profile_profile_change' is not present in the JSON file.")
            
            # Iterate through the profile changes
            for change in data["profile_profile_change"]:
                string_map_data = change.get("string_map_data", {})
                
                # Extract the required fields
                changed = string_map_data.get("Changed", {}).get("value", "")
                new_value = string_map_data.get("New Value", {}).get("value", "")
                change_date_timestamp = string_map_data.get("Change Date", {}).get("timestamp", 0)
                
                # Convert the timestamp to a readable date format
                change_date = datetime.fromtimestamp(change_date_timestamp / 1000).strftime('%Y-%m-%d')
                
                # Append the change to the list
                changes.append((changed, new_value, change_date))
    
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The profile_changes.json file does not exist.")
    except ValueError as ve:
        raise ValueError(f"ValueError: {ve}")
    except Exception as e:
        raise Exception(f"Exception: An unexpected error occurred while processing the file - {e}")
    
    return changes

def save_changes_to_csv(changes, output_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the changes to a CSV file
    with open(output_path, 'w', newline='') as csvfile:
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
        save_changes_to_csv(changes, output_path)
        
        print(f"Results saved to {output_path}")
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()