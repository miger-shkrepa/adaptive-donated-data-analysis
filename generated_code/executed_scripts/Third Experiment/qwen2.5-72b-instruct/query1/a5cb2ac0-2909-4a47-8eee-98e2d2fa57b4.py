import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_directory):
    topics_of_interest = []
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        preferences_path = os.path.join(root_directory, "preferences", "your_topics", "recommended_topics.json")
        
        if not os.path.exists(preferences_path):
            return topics_of_interest  # Return empty list if the file does not exist
        
        with open(preferences_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            topics = data.get("topics_your_topics", [])
            for topic in topics:
                string_map_data = topic.get("string_map_data", {})
                name = string_map_data.get("Name", {}).get("value")
                if name:
                    topics_of_interest.append(name)
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding failed - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")
    
    return topics_of_interest

def write_to_csv(topics, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV - {e}")

if __name__ == "__main__":
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(topics_of_interest, output_path)
    except Exception as e:
        print(e)