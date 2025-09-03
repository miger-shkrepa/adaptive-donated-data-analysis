import os
import json
import csv

root_dir = "root_dir"

def extract_topics_of_interest(root_dir):
    topics_of_interest = []
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        json_file_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")
        
        if not os.path.exists(json_file_path):
            print("Warning: The required JSON file does not exist. Returning a CSV with only headers.")
            return topics_of_interest
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        for topic in data.get("topics_your_topics", []):
            name_value = topic.get("string_map_data", {}).get("Name", {}).get("value")
            if name_value:
                topics_of_interest.append(name_value)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")
    
    return topics_of_interest

def save_to_csv(topics_of_interest):
    csv_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
    
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
        for topic in topics_of_interest:
            writer.writerow([topic])

if __name__ == "__main__":
    try:
        topics_of_interest = extract_topics_of_interest(root_dir)
        save_to_csv(topics_of_interest)
    except Exception as e:
        print(e)