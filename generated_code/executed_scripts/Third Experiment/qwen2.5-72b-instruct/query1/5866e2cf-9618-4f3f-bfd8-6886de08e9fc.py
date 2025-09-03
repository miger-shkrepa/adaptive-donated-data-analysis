import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest():
    topics_of_interest = []
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_info_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "ads_about_meta.json")
        
        if not os.path.exists(ads_info_path):
            print("Warning: ads_about_meta.json not found. Returning an empty list for topics of interest.")
            return topics_of_interest
        
        with open(ads_info_path, 'r') as file:
            data = json.load(file)
            label_values = data.get("label_values", [])
            for item in label_values:
                if "label" in item and "value" in item:
                    topics_of_interest.append(item["value"])
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")
    
    return topics_of_interest

def write_to_csv(topics):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

if __name__ == "__main__":
    try:
        topics = get_topics_of_interest()
        write_to_csv(topics)
    except Exception as e:
        print(e)