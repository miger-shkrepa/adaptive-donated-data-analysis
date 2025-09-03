import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics = set()
    
    ads_and_topics_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'ads_viewed.json')
    
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")
    
    if os.path.exists(ads_and_topics_path):
        try:
            with open(ads_and_topics_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                impressions_history_ads_seen = data.get('impressions_history_ads_seen', [])
                for entry in impressions_history_ads_seen:
                    string_map_data = entry.get('string_map_data', [])
                    for item in string_map_data:
                        if isinstance(item, dict):
                            for key, value in item.items():
                                if key == 'Author' and isinstance(value, dict):
                                    topics.add(value.get('value'))
        except json.JSONDecodeError:
            raise ValueError("Error: Failed to decode JSON in ads_viewed.json.")
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")
    
    return topics

def write_to_csv(topics, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
        for topic in topics:
            writer.writerow([topic])

if __name__ == "__main__":
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest, 'query_responses/results.csv')
    except Exception as e:
        print(e)