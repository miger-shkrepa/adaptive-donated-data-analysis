import json
import os
import csv
from datetime import datetime

def find_file(base_folder, target_file):
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def extract_device_logins(base_folder):
    target_file = "devices.json"
    file_path = find_file(base_folder, target_file)

    if not file_path:
        print(f"Warning: {target_file} not found in {base_folder}. Skipping.")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    devices = data.get("devices_devices", [])
    device_info = []
    for entry in devices:
        string_map = entry.get("string_map_data", {})
        device_id = string_map.get("User Agent", {}).get("value")
        login_ts = string_map.get("Last Login", {}).get("timestamp")
        if device_id and login_ts:
            login_time = datetime.fromtimestamp(login_ts).strftime("%Y-%m-%d %H:%M:%S")
            device_info.append((device_id, login_time))

    return device_info

def save_device_logins_to_csv(device_info, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Device ID", "Login Time"])
            for device_id, login_time in device_info:
                writer.writerow([device_id, login_time])
        print(f"✅ Saved: {output_file}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

def main():
    datasets_dir = "../../datasets"
    output_dir = os.path.join("../../ground_truths", "query5")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: Directory '{datasets_dir}' does not exist.")
        return

    for subdir in os.listdir(datasets_dir):
        full_path = os.path.join(datasets_dir, subdir)
        if not os.path.isdir(full_path):
            continue

        device_info = extract_device_logins(full_path)
        if device_info:
            output_file = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
        else:
            output_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")

        save_device_logins_to_csv(device_info, output_file)

if __name__ == "__main__":
    main()
