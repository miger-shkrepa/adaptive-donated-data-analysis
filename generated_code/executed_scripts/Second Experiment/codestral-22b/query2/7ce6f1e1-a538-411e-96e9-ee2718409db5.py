import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")

results = []

# Process ads_viewed.json
ads_viewed_file = os.path.join(ads_info_dir, "ads_viewed.json")
if os.path.exists(ads_viewed_file):
    with open(ads_viewed_file, 'r') as f:
        data = json.load(f)
        for ad in data["impressions_history_ads_seen"]:
            author = ad["string_map_data"]["Author"]["value"]
            if author not in results:
                results.append((author, 1))
            else:
                index = results.index((author,))
                results[index] = (author, results[index][1] + 1)

# Save results to CSV
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(results)