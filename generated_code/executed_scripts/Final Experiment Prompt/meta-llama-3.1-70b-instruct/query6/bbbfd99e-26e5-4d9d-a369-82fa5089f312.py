import json
import csv
import os

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

        # Load the profile changes data from the file
        with open(profile_changes_file, "r") as file:
            data = json.load(file)

        # Extract the profile changes
        profile_changes = []
        for change in data.get("profile_profile_change", []):
            changed = change.get("string_map_data", {}).get("Changed", {}).get("value")
            new_value = change.get("string_map_data", {}).get("New Value", {}).get("value")
            change_date_timestamp = change.get("string_map_data", {}).get("Change Date", {}).get("timestamp")
            if change_date_timestamp:
                # Convert the timestamp to a date string in the format YYYY-MM-DD
                from datetime import datetime
                change_date = datetime.utcfromtimestamp(change_date_timestamp).strftime("%Y-%m-%d")
            else:
                change_date = ""

            # Add the profile change to the list
            profile_changes.append({
                "Changed": changed,
                "New Value": new_value,
                "Change Date": change_date
            })

        return profile_changes

    except json.JSONDecodeError:
        raise ValueError("Error: Failed to parse the JSON file.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(profile_changes, output_file):
    """
    Saves the profile changes to a CSV file.

    Args:
    profile_changes (list): A list of dictionaries containing the changed field, new value, and change date.
    output_file (str): The path to the output CSV file.
    """
    try:
        # Define the column headers
        headers = ["Changed", "New Value", "Change Date"]

        # Write the profile changes to the CSV file
        with open(output_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(profile_changes)

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    # Define the output file path
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