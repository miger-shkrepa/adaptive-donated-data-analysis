import os
import json
import csv

root_dir = "root_dir"

def get_ads_info(root_dir):
    try:
        ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_info_dir):
            raise FileNotFoundError("Error: The ads information directory does not exist.")
        
        company_ads = {}
        for filename in os.listdir(ads_info_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(ads_info_dir, filename)
                with open(file_path, "r") as file:
                    data = json.load(file)
                    if "impressions_history_posts_seen" in data:
                        impressions = data["impressions_history_posts_seen"]
                        for impression in impressions:
                            author = impression["string_map_data"]["Author"]["value"]
                            if author not in company_ads:
                                company_ads[author] = 1
                            else:
                                company_ads[author] += 1
                    elif "impressions_history_videos_watched" in data:
                        impressions = data["impressions_history_videos_watched"]
                        for impression in impressions:
                            author = impression["string_map_data"]["Author"]["value"]
                            if author not in company_ads:
                                company_ads[author] = 1
                            else:
                                company_ads[author] += 1
        
        return company_ads
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

def write_to_csv(company_ads):
    try:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads_viewed in company_ads.items():
                writer.writerow([company, ads_viewed])
    
    except Exception as e:
        raise ValueError(f"Error: {e}")

def main():
    try:
        company_ads = get_ads_info(root_dir)
        if company_ads:
            write_to_csv(company_ads)
        else:
            with open("query_responses/results.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
    
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except Exception as e:
        raise ValueError(f"Error: {e}")

if __name__ == "__main__":
    main()