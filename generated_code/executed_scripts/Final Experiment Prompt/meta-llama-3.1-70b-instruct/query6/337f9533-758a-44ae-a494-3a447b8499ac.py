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
            raise FileNotFoundError("FileNotFoundError: The profile changes file does not exist.")

        # Load the profile changes data
        with open(profile_changes_file, "r") as file:
            data = json.load(file)

        # Extract the profile changes
        profile_changes = data.get("profile_profile_change", [])

        # Initialize the results list
        results = []

        # Iterate over the profile changes
        for change in profile_changes:
            string_map_data = change.get("string_map_data", {})

            # Extract the changed field, new value, and change date
            changed = string_map_data.get("Changed", {}).get("value", "")
            new_value = string_map_data.get("New Value", {}).get("value", "")
            change_date_timestamp = string_map_data.get("Change Date", {}).get("timestamp", 0)

            # Convert the change date timestamp to a date string
            if change_date_timestamp > 0:
                change_date = datetime.utcfromtimestamp(change_date_timestamp).strftime("%Y-%m-%d")
            else:
                change_date = ""

            # Append the result to the results list
            results.append({
                "Changed": changed,
                "New Value": new_value,
                "Change Date": change_date
            })

        return results

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_results_to_csv(results, output_file):
    try:
        # Define the column headers
        column_headers = ["Changed", "New Value", "Change Date"]

        # Write the results to the CSV file
        with open(output_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=column_headers)
            writer.writeheader()
            writer.writerows(results)

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def main():
    try:
        # Get the profile changes
        results = get_profile_changes(root_dir)

        # Save the results to a CSV file
        output_file = "query_responses/results.csv"
        save_results_to_csv(results, output_file)

    except FileNotFoundError as e:
        # If a required file does not exist, save a CSV file with only the column headers
        output_file = "query_responses/results.csv"
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Changed", "New Value", "Change Date"])
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()