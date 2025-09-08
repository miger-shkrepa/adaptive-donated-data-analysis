import os
import json
import csv

root_dir = "root_dir"

def extract_topics(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    topics = []

    # Traverse the directory
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        # Check if the file contains 'interest_topics'
                        if 'ig_reels_media' in data:
                            for item in data['ig_reels_media']:
                                if 'media' in item:
                                    for media in item['media']:
                                        if 'interest_topics' in media:
                                            for topic in media['interest_topics']:
                                                topics.append(topic['topic_name'])
                except Exception as e:
                    print(f"Error processing file {filepath}: {e}")

    return topics

def save_to_csv(topics, output_file='query_responses/results.csv'):
    # Create the directory if it does not exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Topics of Interest'])
        for topic in topics:
            writer.writerow([topic])

topics = extract_topics(root_dir)
save_to_csv(topics)