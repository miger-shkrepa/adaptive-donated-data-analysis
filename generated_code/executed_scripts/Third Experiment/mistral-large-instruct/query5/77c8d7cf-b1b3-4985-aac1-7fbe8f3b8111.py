import os
import json
import csv
from datetime import datetime

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to parse the login times from the JSON files
def parse_login_times(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            login_times = []
            for entry in data.get('devices_devices', []):
                string_map_data = entry.get('string_map_data', {})
                last_login = string_map_data.get('Last Login', {}).get('value')
                if last_login:
                    login_times.append((entry.get('title', 'Unknown'), last_login))
            return login_times
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

# Function to write the results to a CSV file
def write_to_csv(data, file_path):
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Device ID', 'Login Time'])
            for device_id, login_time in data:
                try:
                    # Convert the login time to the required format
                    login_time_obj = datetime.strptime(login_time, '%Y-%m-%dT%H:%M:%S')
                    formatted_time = login_time_obj.strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([device_id, formatted_time])
                except ValueError:
                    writer.writerow([device_id, 'Invalid Time Format'])
    except Exception as e:
        raise IOError(f"IOError: Failed to write to CSV file. {str(e)}")

# Main function to process the directory and generate the CSV
def main():
    try:
        devices_file = os.path.join(root_dir, 'personal_information', 'device_information', 'devices.json')
        if not os.path.exists(devices_file):
            raise FileNotFoundError("FileNotFoundError: The devices.json file does not exist.")

        login_times = parse_login_times(devices_file)
        write_to_csv(login_times, output_csv)

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as val_error:
        print(val_error)
    except IOError as io_error:
        print(io_error)

if __name__ == "__main__":
    main()