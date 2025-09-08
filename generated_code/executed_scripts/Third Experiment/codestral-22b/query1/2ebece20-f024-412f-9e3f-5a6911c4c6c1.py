import os
import json
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

topics_of_interest = []

ads_and_topics_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")

if os.path.exists(ads_and_topics_dir):
    for filename in os.listdir(ads_and_topics_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(ads_and_topics_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    if "string_map_data" in item and "Topic" in item["string_map_data"]:
                        topics_of_interest.append(item["string_map_data"]["Topic"]["value"])

with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])