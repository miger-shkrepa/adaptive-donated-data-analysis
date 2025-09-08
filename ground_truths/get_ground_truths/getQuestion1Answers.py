import json
import os
import csv

def find_recommended_topics_file(main_directory):
    for root, dirs, files in os.walk(main_directory):
        if 'recommended_topics.json' in files:
            return os.path.join(root, 'recommended_topics.json')
    return None

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_recommended_topics(data):
    topics = []
    for topic in data.get('topics_your_topics', []):
        topic_name = topic.get('string_map_data', {}).get('Name', {}).get('value')
        if topic_name:
            topics.append(topic_name)
    return topics

def main():
    datasets_dir = "../../datasets"
    output_dir = os.path.join("../../ground_truths", "query1")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(datasets_dir):
        print(f"Error: The directory '{datasets_dir}' does not exist.")
        return

    for entry in os.listdir(datasets_dir):
        full_path = os.path.join(datasets_dir, entry)
        if not os.path.isdir(full_path):
            continue

        topics_file_path = find_recommended_topics_file(full_path)
        if not topics_file_path:
            output_file = os.path.join(output_dir, f"NODATA_{entry}_ground_truth.csv")
            with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Topics of Interest"])
            print(f"⚠️  No data found. Created empty file: {output_file}")
            continue

        data = load_json(topics_file_path)
        topics = get_recommended_topics(data)

        output_file = os.path.join(output_dir, f"{entry}_ground_truth.csv")
        with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])

        print(f"✅ Saved: {output_file}")

if __name__ == "__main__":
    main()
