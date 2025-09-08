import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_directory):
    topics_of_interest = []
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        locations_of_interest_path = os.path.join(root_directory, "information_about_you", "locations_of_interest.json")
        
        if not os.path.exists(locations_of_interest_path):
            print("Warning: locations_of_interest.json not found. Returning an empty list for topics of interest.")
            return topics_of_interest
        
        with open(locations_of_interest_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            label_values = data.get("label_values", [])
            
            for item in label_values:
                label = item.get("label")
                if label:
                    topics_of_interest.append(label)
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")
    
    return topics_of_interest

def write_to_csv(topics):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV - {e}")

try:
    topics = get_topics_of_interest(root_dir)
    write_to_csv(topics)
except Exception as e:
    print(e)