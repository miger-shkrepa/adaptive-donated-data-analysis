import json
import os
import csv
from datetime import datetime

def find_file(base_folder, target_file):
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def extract_account_changes(base_folder):
    target_file = "profile_changes.json"
    file_path = find_file(base_folder, target_file)

    if not file_path:
        print(f"Warning: {target_file} not found in {base_folder}. Skipping.")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changes = data.get("profile_profile_change", [])
    change_info = []
    for entry in changes:
        string_map = entry.get("string_map_data", {})
        field_changed = string_map.get("Changed", {}).get("value")
        new_value = string_map.get("New Value", {}).get("value")
        change_ts = string_map.get("Change Date", {}).get("timestamp")
        if field_changed and new_value and change_ts:
            change_date = datetime.fromtimestamp(change_ts).strftime("%Y-%m-%d %H:%M:%S")
            change_info.append((field_changed, new_value, change_date))

    return change_info

def save_account_changes_to_csv(change_info, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Changed", "New Value", "Change Date"])
            for changed, new_value, date in change_info:
                writer.writerow([changed, new_value, date])
        print(f"✅ Saved: {output_file}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

def main():
    datasets_dir = "../../datasets"
    output_dir = os.path.join("../../ground_truths", "query6")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: Directory '{datasets_dir}' does not exist.")
        return

    for subdir in os.listdir(datasets_dir):
        full_path = os.path.join(datasets_dir, subdir)
        if not os.path.isdir(full_path):
            continue

        change_info = extract_account_changes(full_path)
        if change_info:
            output_file = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
        else:
            output_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")

        save_account_changes_to_csv(change_info, output_file)

if __name__ == "__main__":
    main()
