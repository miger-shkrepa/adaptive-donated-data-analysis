import json
import csv
import os
from datetime import datetime

root_dir = "root_dir"

def get_device_login_info(root_dir):
    """
    Extracts device login information from the devices.json file.

    Args:
    root_dir (str): The path to the root directory.

    Returns:
    list: A list of tuples containing device ID and login time.
    """
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Construct the path to the devices.json file
        devices_json_path = os.path.join(root_dir, "personal_information", "device_information", "devices.json")

        # Check if the devices.json file exists
        if not os.path.exists(devices_json_path):
            # If the file does not exist, return an empty list
            return []

        # Load the devices.json file
        with open(devices_json_path, "r") as file:
            data = json.load(file)

        # Extract device login information
        device_login_info = []
        for device in data.get("devices_devices", []):
            user_agent = device.get("string_map_data", {}).get("User Agent", {})
            last_login = device.get("string_map_data", {}).get("Last Login", {})

            # Extract device ID from user agent
            device_id = user_agent.get("value", "")

            # Extract login time from last login timestamp
            login_timestamp = last_login.get("timestamp", 0)
            try:
                login_time = datetime.utcfromtimestamp(login_timestamp).strftime("%Y-%m-%d %H:%M:%S")
            except OSError:
                # If the timestamp is invalid, skip this device
                continue

            device_login_info.append((device_id, login_time))

        return device_login_info

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def save_to_csv(device_login_info):
    """
    Saves the device login information to a CSV file.

    Args:
    device_login_info (list): A list of tuples containing device ID and login time.
    """
    try:
        # Create the query_responses directory if it does not exist
        query_responses_dir = "query_responses"
        if not os.path.exists(query_responses_dir):
            os.makedirs(query_responses_dir)

        # Save the device login information to a CSV file
        with open(os.path.join(query_responses_dir, "results.csv"), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
            writer.writerows(device_login_info)

    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def main():
    device_login_info = get_device_login_info(root_dir)
    save_to_csv(device_login_info)

if __name__ == "__main__":
    main()