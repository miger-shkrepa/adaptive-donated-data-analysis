import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

def find_file(directory, filename):
    for root, _, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            import json
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def extract_topics_of_interest(data):
    topics = []
    if 'topics_your_topics' in data:
        for topic in data['topics_your_topics']:
            if 'string_map_data' in topic and 'Name' in topic['string_map_data']:
                topics.append(topic['string_map_data']['Name']['value'])
    return topics

def main():
    try:
        # Find the recommended_topics.json file
        topics_file_path = find_file(root_dir, 'recommended_topics.json')
        if not topics_file_path:
            # If the file is not found, create an empty CSV with the header
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Topics of Interest'])
            return

        # Read the JSON file
        topics_data = read_json_file(topics_file_path)

        # Extract topics of interest
        topics_of_interest = extract_topics_of_interest(topics_data)

        # Write the topics to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()