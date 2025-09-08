import os
import json
import csv

root_dir = "root_dir"

def extract_topics(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    topics = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json"):
                try:
                    with open(os.path.join(root, file), 'r') as f:
                        data = json.load(f)
                        if 'interest_topics' in data:
                            for item in data['interest_topics']:
                                if 'topic_name' in item:
                                    topics.append(item['topic_name'])
                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON in file {file}")

    return topics

def save_to_csv(topics, output_file='query_responses/results.csv'):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Topics of Interest'])
        for topic in topics:
            writer.writerow([topic])

topics = extract_topics(root_dir)
save_to_csv(topics)