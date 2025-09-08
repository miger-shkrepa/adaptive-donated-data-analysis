import os
import json
import csv

root_dir = "root_dir"
output_file = "query_responses/results.csv"

def extract_topics(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    topics = []
    your_topics_dir = os.path.join(root_dir, "preferences", "your_topics")
    your_topics_file = os.path.join(your_topics_dir, "your_topics.json")

    if os.path.exists(your_topics_file):
        with open(your_topics_file, 'r') as f:
            data = json.load(f)
            for topic in data["topics_your_topics"]:
                topics.append(topic["string_map_data"]["Name"]["value"])

    return topics

def save_to_csv(topics, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Topics of Interest"])
        for topic in topics:
            writer.writerow([topic])

try:
    topics = extract_topics(root_dir)
    save_to_csv(topics, output_file)
except Exception as e:
    print(f"Error: {str(e)}")