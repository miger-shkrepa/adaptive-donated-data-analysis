import os
import json
import csv

root_dir = "root_dir"

def find_file(directory, filename):
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)
    return None

def extract_topics_of_interest(file_path):
    topics = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'label_values' in data:
                for item in data['label_values']:
                    if 'label' in item:
                        topics.append(item['label'])
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")
    return topics

def main():
    try:
        locations_of_interest_path = find_file(root_dir, 'locations_of_interest.json')
        if not locations_of_interest_path:
            raise FileNotFoundError("FileNotFoundError: The locations_of_interest.json file does not exist.")
        
        topics_of_interest = extract_topics_of_interest(locations_of_interest_path)
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])
    
    except (FileNotFoundError, ValueError) as e:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])

if __name__ == "__main__":
    main()