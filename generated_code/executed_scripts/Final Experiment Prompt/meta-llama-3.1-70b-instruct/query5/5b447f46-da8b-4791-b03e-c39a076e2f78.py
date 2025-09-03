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
            if login_timestamp > 0:
                login_time = datetime.utcfromtimestamp(login_timestamp).strftime("%Y-%m-%d %H:%M:%S")
            else:
                login_time = ""

            # Add device login information to the list
            device_login_info.append((device_id, login_time))

        return device_login_info

    except json.JSONDecodeError:
        raise ValueError("Error: Failed to parse JSON file.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def save_to_csv(device_login_info):
    """
    Saves the device login information to a CSV file.

    Args:
    device_login_info (list): A list of tuples containing device ID and login time.
    """
    try:
        # Construct the path to the output CSV file
        output_csv_path = "query_responses/results.csv"

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_csv_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the device login information to the CSV file
        with open(output_csv_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Device ID", "Login Time"])
            for device_id, login_time in device_login_info:
                writer.writerow([device_id, login_time])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    device_login_info = get_device_login_info(root_dir)
    save_to_csv(device_login_info)

if __name__ == "__main__":
    main()