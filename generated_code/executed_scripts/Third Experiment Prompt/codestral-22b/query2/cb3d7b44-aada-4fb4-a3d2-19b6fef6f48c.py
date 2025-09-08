import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_data = {}

# Traverse the directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "ads_about_meta.json":
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if 'ads_information' in data and 'instagram_ads_and_businesses' in data['ads_information'] and 'ads_about_meta.json' in data['ads_information']['instagram_ads_and_businesses'] and 'structure' in data['ads_information']['instagram_ads_and_businesses']['ads_about_meta.json'] and 'label_values' in data['ads_information']['instagram_ads_and_businesses']['ads_about_meta.json']['structure']:
                        for item in data['ads_information']['instagram_ads_and_businesses']['ads_about_meta.json']['structure']['label_values']:
                            if item['label'] == 'Advertiser Name':
                                company_name = item['value']
                                if company_name in ads_data:
                                    ads_data[company_name] += 1
                                else:
                                    ads_data[company_name] = 1
            except FileNotFoundError:
                print(f"FileNotFoundError: The file {filepath} does not exist.")
            except json.JSONDecodeError:
                print(f"JSONDecodeError: The file {filepath} is not a valid JSON file.")

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name', 'Number of Ads Viewed'])
    for company_name, count in ads_data.items():
        writer.writerow([company_name, count])