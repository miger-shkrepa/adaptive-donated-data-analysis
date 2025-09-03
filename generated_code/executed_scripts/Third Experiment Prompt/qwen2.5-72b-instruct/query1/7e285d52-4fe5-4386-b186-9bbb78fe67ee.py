import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics = set()
    ads_and_topics_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if os.path.exists(ads_and_topics_path):
        try:
            with open(ads_and_topics_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                impressions_history_ads_seen = data.get('impressions_history_ads_seen', [])
                
                for ad in impressions_history_ads_seen:
                    string_map_data = ad.get('string_map_data', [])
                    for string_map in string_map_data:
                        if isinstance(string_map, dict):
                            for key, value in string_map.items():
                                if key == 'Author' and isinstance(value, dict):
                                    author_value = value.get('value')
                                    if isinstance(author_value, str):
                                        topics.add(author_value)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error: Failed to decode JSON from {ads_and_topics_path}. Reason: {e}")
        except Exception as e:
            raise ValueError(f"Error: An unexpected error occurred while processing {ads_and_topics_path}. Reason: {e}")
    
    return topics

def write_to_csv(topics, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        raise ValueError(f"Error: Failed to write to CSV file. Reason: {e}")

if __name__ == "__main__":
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        output_path = 'query_responses/results.csv'
        write_to_csv(topics_of_interest, output_path)
    except Exception as e:
        print(e)