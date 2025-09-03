import os
import json
import csv

root_dir = "root_dir"

def get_advertisers(root_dir):
    try:
        advertisers = {}
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")
        
        for filename in os.listdir(ads_and_topics_dir):
            if filename == "ads_viewed.json":
                ads_viewed_path = os.path.join(ads_and_topics_dir, filename)
                if not os.path.exists(ads_viewed_path):
                    raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
                
                with open(ads_viewed_path, 'r') as file:
                    ads_viewed_data = json.load(file)
                    for ad in ads_viewed_data["impressions_history_ads_seen"]:
                        if "string_map_data" in ad and "Author" in ad["string_map_data"]:
                            author = ad["string_map_data"]["Author"]["value"]
                            if author not in advertisers:
                                advertisers[author] = 1
                            else:
                                advertisers[author] += 1
        
        return advertisers
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def get_company_names(advertisers):
    try:
        company_names = {}
        instagram_ads_and_businesses_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
        if not os.path.exists(instagram_ads_and_businesses_dir):
            raise FileNotFoundError("FileNotFoundError: The instagram_ads_and_businesses directory does not exist.")
        
        advertisers_using_your_activity_path = os.path.join(instagram_ads_and_businesses_dir, "advertisers_using_your_activity_or_information.json")
        if not os.path.exists(advertisers_using_your_activity_path):
            raise FileNotFoundError("FileNotFoundError: The advertisers_using_your_activity_or_information.json file does not exist.")
        
        with open(advertisers_using_your_activity_path, 'r') as file:
            advertisers_using_your_activity_data = json.load(file)
            for advertiser in advertisers_using_your_activity_data["ig_custom_audiences_all_types"]:
                advertiser_name = advertiser["advertiser_name"]
                company_names[advertiser_name] = 0
        
        return company_names
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        advertisers = get_advertisers(root_dir)
        company_names = get_company_names(advertisers)
        
        for author, count in advertisers.items():
            if author in company_names:
                company_names[author] = count
        
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in company_names.items():
                writer.writerow([company, count])
    
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

if __name__ == "__main__":
    main()