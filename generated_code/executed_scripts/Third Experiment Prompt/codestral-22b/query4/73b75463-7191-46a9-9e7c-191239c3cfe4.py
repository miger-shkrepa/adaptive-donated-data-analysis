import os
import json
import csv

root_dir = "root_dir"
companies = set()

def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if "advertisers_using_your_activity_or_information" in data:
                advertisers = data["advertisers_using_your_activity_or_information"]["structure"]["ig_custom_audiences_all_types"]
                for advertiser in advertisers:
                    companies.add(advertiser["advertiser_name"])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def traverse_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "advertisers_using_your_activity_or_information.json":
                process_file(os.path.join(root, file))

try:
    traverse_directory(root_dir)
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")