import json
import csv
import os

# Define the root directory
root_dir = "root_dir"

def get_profile_changes(root_dir):
    """
    Retrieves profile changes from the profile_changes.json file.

    Args:
    root_dir (str): The path to the root directory.

    Returns:
    list: A list of dictionaries containing the profile changes.
    """
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the profile_changes.json file
        profile_changes_path = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

        # Check if the profile_changes.json file exists
        if not os.path.exists(profile_changes_path):
            return []

        # Open and load the profile_changes.json file
        with open(profile_changes_path, "r") as file:
            data = json.load(file)

        # Return the profile changes
        return data.get("profile_profile_change", [])

    except json.JSONDecodeError:
        raise ValueError("Error: The profile_changes.json file is not a valid JSON file.")

def extract_changes(profile_changes):
    """
    Extracts the changes from the profile changes.

    Args:
    profile_changes (list): A list of dictionaries containing the profile changes.

    Returns:
    list: A list of dictionaries containing the extracted changes.
    """
    changes = []
    for change in profile_changes:
        string_map_data = change.get("string_map_data", {})
        changed = string_map_data.get("Changed", {}).get("value", "")
        new_value = string_map_data.get("New Value", {}).get("value", "")
        change_date_timestamp = string_map_data.get("Change Date", {}).get("timestamp", 0)
        change_date = ""
        try:
            # Convert the timestamp to a date in the format YYYY-MM-DD
            import datetime
            change_date = datetime.datetime.fromtimestamp(change_date_timestamp).strftime("%Y-%m-%d")
        except OSError:
            # Handle invalid timestamp
            pass

        changes.append({
            "Changed": changed,
            "New Value": new_value,
            "Change Date": change_date
        })

    return changes

def save_changes_to_csv(changes, output_path):
    """
    Saves the changes to a CSV file.

    Args:
    changes (list): A list of dictionaries containing the changes.
    output_path (str): The path to the output CSV file.
    """
    # Create the output directory if it does not exist
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open and write to the output CSV file
    with open(output_path, "w", newline="") as file:
        fieldnames = ["Changed", "New Value", "Change Date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(changes)

def main():
    # Get the profile changes
    profile_changes = get_profile_changes(root_dir)

    # Extract the changes
    changes = extract_changes(profile_changes)

    # Save the changes to a CSV file
    output_path = "query_responses/results.csv"
    save_changes_to_csv(changes, output_path)

if __name__ == "__main__":
    main()