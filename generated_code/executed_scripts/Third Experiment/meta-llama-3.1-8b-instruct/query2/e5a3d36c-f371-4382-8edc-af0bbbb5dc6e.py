import csv
import os

root_dir = "root_dir"

try:
    root_dir = os.path.abspath(root_dir)
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except Exception as e:
    raise

ads_info = {}
for file in os.listdir(root_dir):
    file_path = os.path.join(root_dir, file)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            if 'ads_and_topics' in data:
                for file_name, info in data['ads_and_topics'].items():
                    if info['type'] == 'json':
                        for item in info['structure']['impressions_history_ads_seen']:
                            author = item['string_map_data']['Author']['value']
                            if author not in ads_info:
                                ads_info[author] = 0
                            ads_info[author] += 1

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Company Name', 'Number of Ads Viewed'])
    for author, count in ads_info.items():
        writer.writerow([author, count])