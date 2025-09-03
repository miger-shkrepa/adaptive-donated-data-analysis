import csv
import os

def get_ads_info(root_dir):
    ads_info = {}
    for file in os.listdir(root_dir):
        if file.endswith(".json"):
            with open(os.path.join(root_dir, file), 'r') as f:
                data = eval(f.read())
                if 'ads_and_topics' in data['ads_information']:
                    for ad, topics in data['ads_information']['ads_and_topics'].items():
                        if ad == 'ads_viewed.json':
                            for impression in topics['structure']['impressions_history_ads_seen']:
                                author = impression['string_map_data']['Author']['value']
                                if author not in ads_info:
                                    ads_info[author] = {'Company Name': author, 'Number of Ads Viewed': 0}
                                ads_info[author]['Number of Ads Viewed'] += 1
    return ads_info

def write_to_csv(ads_info):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company, info in ads_info.items():
            writer.writerow(info)

def main():
    root_dir = "root_dir"
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        print(f"Error: {e}")
        return

    ads_info = get_ads_info(root_dir)
    write_to_csv(ads_info)

if __name__ == "__main__":
    main()