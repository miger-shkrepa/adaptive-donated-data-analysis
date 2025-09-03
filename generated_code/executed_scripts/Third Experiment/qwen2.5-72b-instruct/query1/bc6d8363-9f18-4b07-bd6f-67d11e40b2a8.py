import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_directory):
    topics_of_interest = []
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        topics_file_path = os.path.join(root_directory, "topics_of_interest.json")
        
        if not os.path.exists(topics_file_path):
            return topics_of_interest  # Return empty list if the file does not exist
        
        with open(topics_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            if 'topics' in data:
                topics_of_interest = data['topics']
            else:
                raise ValueError("Error: The JSON file does not contain the expected 'topics' key.")
                
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
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
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

if __name__ == "__main__":
    try:
        topics = get_topics_of_interest(root_dir)
        write_to_csv(topics, 'query_responses/results.csv')
    except Exception as e:
        print(e)