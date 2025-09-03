import csv
import json

root_dir = "root_dir"

try:
    with open(f"{root_dir}/preferences/your_topics/recommended_topics.json", 'r') as f:
        data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

topics_of_interest = []
for topic in data["topics_your_topics"]:
    try:
        topics_of_interest.append(topic["string_map_data"]["Name"]["value"])
    except KeyError:
        # If the file is incomplete or partially missing, treat the contribution as 0
        pass

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])  # Write column headers
    writer.writerows([[topic] for topic in topics_of_interest])  # Write topics of interest