import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_directory):
    topics_of_interest = set()
    ads_and_topics_path = os.path.join(root_directory, "ads_information", "ads_and_topics")
    
    if not os.path.exists(root_directory):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    if not os.path.exists(ads_and_topics_path):
        return topics_of_interest

    for filename in os.listdir(ads_and_topics_path):
        if filename.endswith(".json"):
            file_path = os.path.join(ads_and_topics_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if "impressions_history_ads_seen" in data:
                        for entry in data["impressions_history_ads_seen"]:
                            for string_map in entry.get("string_map_data", {}).values():
                                if isinstance(string_map, dict) and "value" in string_map:
                                    topics_of_interest.add(string_map["value"])
                    elif "impressions_history_app_message" in data:
                        for entry in data["impressions_history_app_message"]:
                            for string_map in entry.get("string_map_data", {}).values():
                                if isinstance(string_map, dict) and "value" in string_map:
                                    topics_of_interest.add(string_map["value"])
                    # Add similar checks for other relevant keys as necessary
            except json.JSONDecodeError:
                raise ValueError("Error: Failed to decode JSON file.")
            except Exception as e:
                raise ValueError(f"Error: {str(e)}")

    return topics_of_interest

def write_to_csv(topics, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics:
            writer.writerow([topic])

try:
    topics = get_topics_of_interest(root_dir)
    write_to_csv(topics, 'query_responses/results.csv')
except Exception as e:
    print(e)