import csv
import os

root_dir = "root_dir"

def get_ads_info(root_dir):
    try:
        ads_info = {}
        for file in os.listdir(root_dir):
            file_path = os.path.join(root_dir, file)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'ads_and_topics' in data:
                        for ad_file in data['ads_and_topics'].values():
                            if ad_file['type'] == 'json':
                                ad_name = ad_file['structure']['impressions_history_ads_seen'][0]['string_map_data']['Author']['value']
                                if ad_name not in ads_info:
                                    ads_info[ad_name] = 0
                                ads_info[ad_name] += 1
        return ads_info
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: Invalid JSON format in file.")

def save_to_csv(ads_info):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in ads_info.items():
            writer.writerow([company, count])

def main():
    ads_info = get_ads_info(root_dir)
    save_to_csv(ads_info)

if __name__ == "__main__":
    main()