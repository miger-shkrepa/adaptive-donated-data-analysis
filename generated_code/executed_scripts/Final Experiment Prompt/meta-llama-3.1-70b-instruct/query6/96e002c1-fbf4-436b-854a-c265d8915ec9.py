import json
import csv
import os
from datetime import datetime

root_dir = "root_dir"

def get_profile_changes(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the profile changes file
        profile_changes_file = os.path.join(root_dir, "personal_information", "personal_information", "profile_changes.json")

        # Check if the profile changes file exists
        if not os.path.exists(profile_changes_file):
            # If the file does not exist, return an empty list
            return []

        # Open and read the profile changes file
        with open(profile_changes_file, "r") as file:
            data = json.load(file)

        # Extract the profile changes
        profile_changes = data.get("profile_profile_change", [])

        # Initialize the results list
        results = []

        # Iterate over the profile changes
        for change in profile_changes:
            # Extract the changed field, new value, and change date
            changed = change["string_map_data"].get("Changed", {}).get("value")
            new_value = change["string_map_data"].get("New Value", {}).get("value")
            change_date_timestamp = change["string_map_data"].get("Change Date", {}).get("timestamp")

            # Convert the change date timestamp to a date string
            if change_date_timestamp:
                change_date = datetime.utcfromtimestamp(change_date_timestamp).strftime("%Y-%m-%d")
            else:
                change_date = ""

            # Append the result to the results list
            results.append((changed, new_value, change_date))

        return results

    except json.JSONDecodeError:
        raise ValueError("Error: The profile changes file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_results_to_csv(results):
    try:
        # Define the path to the results CSV file
        results_file = "query_responses/results.csv"

        # Create the query_responses directory if it does not exist
        results_dir = os.path.dirname(results_file)
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Open and write the results to the CSV file
        with open(results_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Changed", "New Value", "Change Date"])  # Write the header
            writer.writerows(results)

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        # Get the profile changes
        results = get_profile_changes(root_dir)

        # Save the results to a CSV file
        save_results_to_csv(results)

    except Exception as e:
        # If an error occurs, save an empty CSV file with only the column headers
        save_results_to_csv([])

if __name__ == "__main__":
    main()