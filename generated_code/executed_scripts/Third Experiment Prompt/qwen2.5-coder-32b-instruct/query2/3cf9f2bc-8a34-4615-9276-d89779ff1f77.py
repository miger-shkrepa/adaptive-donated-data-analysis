import os
import csv
import json

# Variable referring to the file input
root_dir = "root_dir"

def get_ads_viewed_data(root_dir):
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(ads_viewed_path):
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    
    with open(ads_viewed_path, 'r', encoding='utf-8') as file:
        ads_viewed_data = json.load(file)
    
    return ads_viewed_data

def process_ads_viewed_data(ads_viewed_data):
    company_ads_count = {}
    
    if "impressions_history_ads_seen" in ads_viewed_data:
        for ad in ads_viewed_data["impressions_history_ads_seen"]:
            if "string_map_data" in ad and "Author" in ad["string_map_data"]:
                author = ad["string_map_data"]["Author"]["value"]
                if author not in company_ads_count:
                    company_ads_count[author] = 0
                company_ads_count[author] += 1
    
    return company_ads_count

def save_to_csv(company_ads_count, output_path):
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for company, count in company_ads_count.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

def main():
    try:
        ads_viewed_data = get_ads_viewed_data(root_dir)
        company_ads_count = process_ads_viewed_data(ads_viewed_data)
        save_to_csv(company_ads_count, 'query_responses/results.csv')
    except FileNotFoundError as e:
        save_to_csv({}, 'query_responses/results.csv')
        print(e)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()