import os
import json
import csv

root_dir = "root_dir"

def get_company_ads(root_dir):
    company_ads = {}
    try:
        ads_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
        if os.path.exists(ads_path):
            with open(ads_path, 'r') as f:
                data = json.load(f)
                for post in data['impressions_history_posts_seen']:
                    author = post['string_map_data']['Author']['value']
                    if author not in company_ads:
                        company_ads[author] = 1
                    else:
                        company_ads[author] += 1
        else:
            raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))
    return company_ads

def get_company_topics(root_dir):
    company_topics = {}
    try:
        topics_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'advertisers_using_your_activity_or_information.json')
        if os.path.exists(topics_path):
            with open(topics_path, 'r') as f:
                data = json.load(f)
                for advertiser in data['ig_custom_audiences_all_types']:
                    advertiser_name = advertiser['advertiser_name']
                    if advertiser_name not in company_topics:
                        company_topics[advertiser_name] = []
                    company_topics[advertiser_name].append('Custom Audience')
                    if advertiser['has_remarketing_custom_audience']:
                        company_topics[advertiser_name].append('Remarking Custom Audience')
                    if advertiser['has_in_person_store_visit']:
                        company_topics[advertiser_name].append('In Person Store Visit')
        else:
            raise FileNotFoundError("FileNotFoundError: The advertisers_using_your_activity_or_information.json file does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))
    return company_topics

def write_to_csv(company_ads, company_topics):
    try:
        with open('query_responses/results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
            for company, ads in company_ads.items():
                topics = ', '.join(company_topics.get(company, []))
                writer.writerow([company + ' - ' + topics, ads])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        company_ads = get_company_ads(root_dir)
        company_topics = get_company_topics(root_dir)
        write_to_csv(company_ads, company_topics)
    except Exception as e:
        with open('query_responses/results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Company Name', 'Number of Ads Viewed'])
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()