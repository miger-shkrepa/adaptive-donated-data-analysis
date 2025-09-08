import os
import json
import csv

root_dir = "root_dir"

def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            ads_viewed = data.get("impressions_history_ads_seen", [])
            return len(ads_viewed)
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def process_ads_and_topics(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            ads_and_topics = data.get("impressions_history_recs_hidden_authors", [])
            company_ads = {}
            for ad in ads_and_topics:
                company = ad.get("string_map_data", {}).get("Benutzername", {}).get("value")
                if company:
                    company_ads[company] = company_ads.get(company, 0) + 1
            return company_ads
    except FileNotFoundError:
        raise FileNotFoundError("Error: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def generate_csv(company_ads, ads_viewed_count):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if not company_ads:
                return
            for company, count in company_ads.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        ads_and_topics_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "accounts_you're_not_interested_in.json")

        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        ads_viewed_count = 0
        company_ads = {}

        if os.path.exists(ads_viewed_path):
            ads_viewed_count = process_ads_viewed(ads_viewed_path)

        if os.path.exists(ads_and_topics_path):
            company_ads = process_ads_and_topics(ads_and_topics_path)

        generate_csv(company_ads, ads_viewed_count)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()