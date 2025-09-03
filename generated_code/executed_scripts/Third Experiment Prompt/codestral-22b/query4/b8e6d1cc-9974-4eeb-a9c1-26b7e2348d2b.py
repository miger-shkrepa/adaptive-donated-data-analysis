import os
import csv
import json

root_dir = "root_dir"
output_file = "query_responses/results.csv"

def extract_companies(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    companies = set()

    ads_dir = os.path.join(root_dir, "ads_information")
    if os.path.exists(ads_dir):
        ads_topics_dir = os.path.join(ads_dir, "ads_and_topics")
        if os.path.exists(ads_topics_dir):
            for file_name in os.listdir(ads_topics_dir):
                if file_name.endswith(".json"):
                    file_path = os.path.join(ads_topics_dir, file_name)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for item in data.get("impressions_history_posts_seen", []):
                            company = item["string_map_data"]["Author"]["value"]
                            companies.add(company)

        instagram_ads_dir = os.path.join(ads_dir, "instagram_ads_and_businesses")
        if os.path.exists(instagram_ads_dir):
            for file_name in os.listdir(instagram_ads_dir):
                if file_name.endswith(".json"):
                    file_path = os.path.join(instagram_ads_dir, file_name)
                    with open(file_path, "r") as file:
                        data = json.load(file)
                        for item in data.get("label_values", []):
                            company = item["value"]
                            companies.add(company)

    return list(companies)

def save_to_csv(companies, output_file):
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name"])
        for company in companies:
            writer.writerow([company])

companies = extract_companies(root_dir)
save_to_csv(companies, output_file)