import os
import json
import csv

root_dir = "root_dir"

def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            ads_viewed = data.get("impressions_history_ads_seen", [])
            ad_counts = {}
            for ad in ads_viewed:
                string_map_data = ad.get("string_map_data", {})
                author = string_map_data.get("Author", {}).get("value")
                if author:
                    ad_counts[author] = ad_counts.get(author, 0) + 1
            return ad_counts
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def generate_csv(ad_counts):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if ad_counts:
                for company, count in ad_counts.items():
                    writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_viewed_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Company Name', 'Number of Ads Viewed']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return
        
        ad_counts = process_ads_viewed(ads_viewed_path)
        generate_csv(ad_counts)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()