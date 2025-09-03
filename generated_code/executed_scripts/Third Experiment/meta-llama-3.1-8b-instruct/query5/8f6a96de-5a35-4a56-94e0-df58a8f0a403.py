import csv
import os
import json

root_dir = "root_dir"

def get_login_times(root_dir):
    try:
        with os.scandir(root_dir) as entries:
            for entry in entries:
                if entry.is_dir():
                    yield from get_login_times(os.path.join(root_dir, entry.name))
                elif entry.is_file():
                    if entry.name == "devices.json":
                        with open(os.path.join(root_dir, entry.name), 'r') as f:
                            data = json.load(f)
                            for device in data['devices_devices']:
                                login_time = device['string_map_data']['Last Login']['value']
                                yield device['string_map_data']['User Agent']['value'], login_time
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

def write_to_csv(data):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Device ID", "Login Time"])
        writer.writerows(data)

def main():
    data = list(get_login_times(root_dir))
    write_to_csv(data)

if __name__ == "__main__":
    main()