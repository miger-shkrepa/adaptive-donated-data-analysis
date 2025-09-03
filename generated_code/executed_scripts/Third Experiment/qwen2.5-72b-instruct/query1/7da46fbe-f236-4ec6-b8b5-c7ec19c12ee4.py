import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root):
    topics = []
    ads_and_topics_path = os.path.join(root, "ads_information", "ads_and_topics")
    
    if not os.path.exists(ads_and_topics_path):
        raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")
    
    ads_viewed_file = os.path.join(ads_and_topics_path, "ads_viewed.json")
    if not os.path.exists(ads_viewed_file):
        return topics  # Return empty list if the file is missing
    
    try:
        with open(ads_viewed_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for entry in data.get("impressions_history_ads_seen", []):
                for key, value in entry.get("string_map_data", {}).items():
                    if key == "Author":
                        topics.append(value.get("value", ""))
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON from ads_viewed.json.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing ads_viewed.json: {str(e)}")
    
    return topics

def write_to_csv(topics, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to CSV: {str(e)}")

if __name__ == "__main__":
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        topics_of_interest = get_topics_of_interest(root_dir)
        output_csv_path = 'query_responses/results.csv'
        write_to_csv(topics_of_interest, output_csv_path)
    except Exception as e:
        print(str(e))