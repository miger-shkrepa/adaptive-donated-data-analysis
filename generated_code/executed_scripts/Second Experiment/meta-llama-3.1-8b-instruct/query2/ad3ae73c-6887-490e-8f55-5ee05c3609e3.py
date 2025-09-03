import csv
import os

def get_ads_info(root_dir):
    ads_info = {}
    for file in os.listdir(root_dir):
        if file.endswith(".json"):
            with open(os.path.join(root_dir, file), 'r') as f:
                data = eval(f.read())
                if 'ads_and_topics' in data['ads_information']:
                    for ad in data['ads_information']['ads_and_topics'].values():
                        if ad['type'] == 'json':
                            for impression in ad['structure']['impressions_history_ads_seen']:
                                if 'Author' in impression['string_map_data']:
                                    author = impression['string_map_data']['Author']['value']
                                    if author not in ads_info:
                                        ads_info[author] = 1
                                    else:
                                        ads_info[author] += 1
    return ads_info

def write_to_csv(ads_info):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in ads_info.items():
            writer.writerow([company, count])

def main():
    try:
        root_dir = "root_dir"
        ads_info = get_ads_info(root_dir)
        write_to_csv(ads_info)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the data.")

if __name__ == "__main__":
    main()