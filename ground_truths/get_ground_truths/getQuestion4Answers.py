import json
import os
import csv

def find_file(base_folder, target_file):
    for root, _, files in os.walk(base_folder):
        if target_file in files:
            return os.path.join(root, target_file)
    return None

def extract_companies_with_access(base_folder):
    target_file = "advertisers_using_your_activity_or_information.json"
    file_path = find_file(base_folder, target_file)

    if not file_path:
        print(f"Warning: {target_file} not found in {base_folder}. Skipping.")
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    advertisers = data.get("ig_custom_audiences_all_types", [])
    companies = [entry.get("advertiser_name") for entry in advertisers if entry.get("advertiser_name")]

    return companies

def save_companies_to_csv(companies, output_file):
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Company Name"])
            for company in companies:
                writer.writerow([company])
        print(f"✅ Saved: {output_file}")
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")

def main():
    datasets_dir = "../../datasets"
    output_dir = os.path.join("../../ground_truths", "query4")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: Directory '{datasets_dir}' does not exist.")
        return

    for subdir in os.listdir(datasets_dir):
        full_path = os.path.join(datasets_dir, subdir)
        if not os.path.isdir(full_path):
            continue

        companies = extract_companies_with_access(full_path)

        if companies is None:
            output_file = os.path.join(output_dir, f"NODATA_{subdir}_ground_truth.csv")
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Company Name"])
            print(f"⚠️ No data file found. Created placeholder: {output_file}")
            continue

        if not companies:
            continue

        output_file = os.path.join(output_dir, f"{subdir}_ground_truth.csv")
        save_companies_to_csv(companies, output_file)

if __name__ == "__main__":
    main()
