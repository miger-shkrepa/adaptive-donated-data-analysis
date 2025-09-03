import json
import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

def get_profile_changes(root_dir):
    """
    Retrieves profile changes from the given root directory.

    Args:
    root_dir (str): The path to the root directory.

    Returns:
    list: A list of dictionaries containing the changed field, new value, and change date.
    """
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the profile changes file
        profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

        # Check if the profile changes file exists
        if not os.path.exists(profile_changes_file):
            return []

        # Load the profile changes data
        with open(profile_changes_file, "r") as file:
            data = json.load(file)

        # Extract the profile changes
        profile_changes = []
        for change in data.get("profile_profile_change", []):
            string_map_data = change.get("string_map_data", {})
            changed = string_map_data.get("Changed", {}).get("value", "")
            new_value = string_map_data.get("New Value", {}).get("value", "")
            change_date_timestamp = string_map_data.get("Change Date", {}).get("timestamp", 0)
            change_date = datetime.datetime.fromtimestamp(change_date_timestamp).strftime("%Y-%m-%d")
            profile_changes.append({
                "Changed": changed,
                "New Value": new_value,
                "Change Date": change_date
            })

        return profile_changes

    except Exception as e:
        raise ValueError("Error: An error occurred while retrieving profile changes: " + str(e))

def save_to_csv(profile_changes, output_file):
    """
    Saves the profile changes to a CSV file.

    Args:
    profile_changes (list): A list of dictionaries containing the changed field, new value, and change date.
    output_file (str): The path to the output CSV file.
    """
    try:
        # Define the CSV headers
        headers = ["Changed", "New Value", "Change Date"]

        # Save the profile changes to the CSV file
        with open(output_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(profile_changes)

    except Exception as e:
        raise ValueError("Error: An error occurred while saving to CSV: " + str(e))

def main():
    # Define the output CSV file
    output_file = "query_responses/results.csv"

    # Create the output directory if it does not exist
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the profile changes
    profile_changes = get_profile_changes(root_dir)

    # Save the profile changes to the CSV file
    save_to_csv(profile_changes, output_file)

if __name__ == "__main__":
    main()