import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    topics_of_interest = []
    topics_file = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")

    if os.path.exists(topics_file):
        with open(topics_file, 'r') as f:
            data = json.load(f)
            if "topics_your_topics" in data:
                for topic in data["topics_your_topics"]:
                    if "string_map_data" in topic and "Name" in topic["string_map_data"]:
                        topics_of_interest.append(topic["string_map_data"]["Name"]["value"])

    return topics_of_interest

def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Topics of Interest"])
        for item in data:
            writer.writerow([item])

topics_of_interest = get_topics_of_interest(root_dir)
save_to_csv(topics_of_interest, "query_responses/results.csv")