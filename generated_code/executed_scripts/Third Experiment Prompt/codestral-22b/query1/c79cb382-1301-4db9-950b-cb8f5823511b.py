import os
import json
import csv

root_dir = "root_dir"
output_file = "query_responses/results.csv"

def get_topics_of_interest(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    topics_of_interest = []
    topics_file = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

    if os.path.exists(topics_file):
        with open(topics_file, 'r') as f:
            data = json.load(f)
            if "topics_your_topics" in data:
                for topic in data["topics_your_topics"]:
                    if "string_map_data" in topic and "Name" in topic["string_map_data"]:
                        topics_of_interest.append(topic["string_map_data"]["Name"]["value"])

    return topics_of_interest

def save_to_csv(topics_of_interest, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

topics_of_interest = get_topics_of_interest(root_dir)
save_to_csv(topics_of_interest, output_file)