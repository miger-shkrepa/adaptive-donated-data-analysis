import os
import csv
from datetime import datetime

root_dir = "root_dir"

def get_instagram_account_changes(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize lists to store changes
        changes = []
        headers = ["Changed", "New Value", "Change Date"]

        # Check if personal_information directory exists
        personal_info_dir = os.path.join(root_dir, "personal_information")
        if os.path.exists(personal_info_dir):
            # Check if instagram_profile_information.json exists
            instagram_profile_info_file = os.path.join(personal_info_dir, "instagram_profile_information.json")
            if os.path.exists(instagram_profile_info_file):
                try:
                    # Open and read instagram_profile_information.json
                    with open(instagram_profile_info_file, "r") as file:
                        # Since we don't have the actual JSON data, we'll assume it's in the correct format
                        # and parse it accordingly
                        data = eval(file.read())
                        for profile_account_insights in data["profile_account_insights"]:
                            string_map_data = profile_account_insights["string_map_data"]
                            for key, value in string_map_data.items():
                                if key in ["Contact Syncing", "First Close Friends Story Time", "First Country Code", 
                                           "First Story Time", "Has Shared Live Video", "Last Login", "Last Logout", 
                                           "Last Story Time"]:
                                    changes.append([key, value["value"], datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")])
                except Exception as e:
                    raise ValueError("ValueError: Failed to parse instagram_profile_information.json - " + str(e))
            else:
                # If instagram_profile_information.json does not exist, skip it
                pass

            # Check if personal_information.json exists
            personal_info_file = os.path.join(personal_info_dir, "personal_information.json")
            if os.path.exists(personal_info_file):
                try:
                    # Open and read personal_information.json
                    with open(personal_info_file, "r") as file:
                        # Since we don't have the actual JSON data, we'll assume it's in the correct format
                        # and parse it accordingly
                        data = eval(file.read())
                        for profile_user in data["profile_user"]:
                            string_map_data = profile_user["string_map_data"]
                            for key, value in string_map_data.items():
                                if key in ["Bio", "Date of birth"]:
                                    changes.append([key, value["value"], datetime.fromtimestamp(value["timestamp"]).strftime("%Y-%m-%d")])
                except Exception as e:
                    raise ValueError("ValueError: Failed to parse personal_information.json - " + str(e))
            else:
                # If personal_information.json does not exist, skip it
                pass
        else:
            # If personal_information directory does not exist, return only headers
            changes = [headers]

        # Save changes to CSV file
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for change in changes:
                if change != headers:
                    writer.writerow(change)

    except Exception as e:
        raise Exception("Error: " + str(e))

get_instagram_account_changes(root_dir)