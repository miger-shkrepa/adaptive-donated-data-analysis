import os
import json
import csv

root_dir = "root_dir"

def get_company_ads_viewed(root_dir):
    company_ads_viewed = {}
    try:
        ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_dir):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")
        
        for filename in os.listdir(ads_and_topics_dir):
            if filename == "ads_viewed.json":
                ads_viewed_file = os.path.join(ads_and_topics_dir, filename)
                if not os.path.exists(ads_viewed_file):
                    raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
                
                with open(ads_viewed_file, 'r') as file:
                    data = json.load(file)
                    for ad in data["impressions_history_ads_seen"]:
                        author = ad["string_map_data"]["Author"]["value"]
                        if author not in company_ads_viewed:
                            company_ads_viewed[author] = 1
                        else:
                            company_ads_viewed[author] += 1
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))
    
    return company_ads_viewed

def write_to_csv(company_ads_viewed):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads_viewed.items():
                writer.writerow([company, ads_viewed])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        company_ads_viewed = get_company_ads_viewed(root_dir)
        if not company_ads_viewed:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
        else:
            write_to_csv(company_ads_viewed)
    except FileNotFoundError as e:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()