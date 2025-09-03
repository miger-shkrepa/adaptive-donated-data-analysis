import os
import csv
import json

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
        
        with open(ads_viewed_path, 'r') as file:
            ads_viewed_data = json.load(file)
        
        ads_viewed_count = {}
        for ad in ads_viewed_data["impressions_history_ads_seen"]:
            if "string_map_data" in ad:
                author = ad["string_map_data"].get("Author", {}).get("value", "")
                if author:
                    if author not in ads_viewed_count:
                        ads_viewed_count[author] = 1
                    else:
                        ads_viewed_count[author] += 1
        
        return ads_viewed_count
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def write_to_csv(ads_viewed_count):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in ads_viewed_count.items():
                writer.writerow([company, count])
    
    except Exception as e:
        raise ValueError(f"Error: {e}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_viewed_count = get_ads_viewed(root_dir)
        if ads_viewed_count:
            write_to_csv(ads_viewed_count)
        else:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
    
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError(f"Error: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

if __name__ == "__main__":
    main()