import os
import json
import csv

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")

def process_ads_data(root_dir):
    ads_data = {}
    ads_info_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses')

    if not os.path.exists(ads_info_path):
        return ads_data

    for json_file in ['ads_about_meta.json', 'other_categories_used_to_reach_you.json']:
        file_path = os.path.join(ads_info_path, json_file)
        if not os.path.exists(file_path):
            continue

        data = load_json(file_path)
        if 'label_values' in data:
            for label_value in data['label_values']:
                if 'label' in label_value and 'value' in label_value:
                    company = label_value['label']
                    ads_data[company] = ads_data.get(company, 0) + 1

    return ads_data

def write_to_csv(data, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, count in data.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        ads_data = process_ads_data(root_dir)
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        write_to_csv(ads_data, output_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()