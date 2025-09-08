import csv
import os

root_dir = "root_dir"

def get_ads_info(root_dir):
    try:
        ads_info = {}
        for file in os.listdir(root_dir):
            file_path = os.path.join(root_dir, file)
            if os.path.isfile(file_path):
                if file.endswith(".json"):
                    with open(file_path, 'r') as f:
                        data = eval(f.read())
                        if 'ads_information' in data and 'ads_and_topics' in data['ads_information']:
                            for file in data['ads_information']['ads_and_topics']:
                                if file.endswith(".json"):
                                    with open(os.path.join(root_dir, file), 'r') as f:
                                        data = eval(f.read())
                                        for item in data['structure']['impressions_history_recs_hidden_authors']:
                                            if 'string_map_data' in item:
                                                company_name = item['string_map_data']['Benutzername']['value']
                                                if company_name not in ads_info:
                                                    ads_info[company_name] = 0
                                                ads_info[company_name] += 1
        return ads_info
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("ValueError: " + str(e))

def write_to_csv(ads_info):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, count in ads_info.items():
            writer.writerow([company, count])

def main():
    ads_info = get_ads_info(root_dir)
    if not ads_info:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
    else:
        write_to_csv(ads_info)

if __name__ == "__main__":
    main()