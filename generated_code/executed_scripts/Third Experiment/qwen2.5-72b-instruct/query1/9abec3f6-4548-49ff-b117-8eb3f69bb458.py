import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_directory):
    topics_of_interest = []
    try:
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_info_path = os.path.join(root_directory, "ads_information", "ads_and_topics", "other_categories_used_to_reach_you.json")
        
        if not os.path.exists(ads_info_path):
            print("Warning: The file 'other_categories_used_to_reach_you.json' does not exist. Returning an empty list for topics of interest.")
            return topics_of_interest
        
        with open(ads_info_path, 'r') as file:
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

def write_to_csv(topics, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
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