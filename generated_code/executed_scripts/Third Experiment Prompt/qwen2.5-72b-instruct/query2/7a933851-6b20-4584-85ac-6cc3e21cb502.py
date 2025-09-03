import os
import json
import csv

root_dir = "root_dir"

def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            ads_viewed = data.get("impressions_history_ads_seen", [])
            company_ads = {}
            for ad in ads_viewed:
                string_map_data = ad.get("string_map_data", {})
                author = string_map_data.get("Author", {}).get("value")
                if author:
                    company_ads[author] = company_ads.get(author, 0) + 1
            return company_ads
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def generate_csv(company_ads):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if company_ads:
                for company, count in company_ads.items():
                    writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        if not os.path.exists(ads_viewed_path):
            generate_csv({})
            return

        company_ads = process_ads_viewed(ads_viewed_path)
        generate_csv(company_ads)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()