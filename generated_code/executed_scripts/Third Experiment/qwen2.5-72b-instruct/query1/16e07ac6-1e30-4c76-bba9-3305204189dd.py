import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics_of_interest = []
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        ads_info_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "other_categories_used_to_reach_you.json")
        
        if not os.path.exists(ads_info_path):
            return topics_of_interest  # Return empty list if the file is not found
        
        with open(ads_info_path, 'r') as file:
            data = json.load(file)
            label_values = data.get("label_values", [])
            
            for item in label_values:
                label = item.get("label")
                vec = item.get("vec", [])
                for value in vec:
                    topics_of_interest.append(value.get("value"))
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {str(e)}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")
    
    return topics_of_interest

def write_to_csv(topics_of_interest):
    file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

try:
    topics_of_interest = get_topics_of_interest(root_dir)
    write_to_csv(topics_of_interest)
except Exception as e:
    print(str(e))