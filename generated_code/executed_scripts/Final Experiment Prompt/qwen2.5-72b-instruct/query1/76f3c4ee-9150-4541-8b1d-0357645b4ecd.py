import os
import json
import csv

root_dir = "root_dir"

def extract_topics_of_interest(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        topics_file_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")
        
        if not os.path.exists(topics_file_path):
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Topics of Interest'])
            return
        
        with open(topics_file_path, 'r') as file:
            data = json.load(file)
        
        topics_of_interest = []
        for topic in data.get("topics_your_topics", []):
            name_value = topic.get("string_map_data", {}).get("Name", {}).get("value")
            if name_value:
                topics_of_interest.append(name_value)
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Call the function with the root directory
extract_topics_of_interest(root_dir)