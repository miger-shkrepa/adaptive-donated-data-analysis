import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root):
    topics = set()
    ads_and_topics_path = os.path.join(root, "ads_information", "ads_and_topics")
    
    if not os.path.exists(ads_and_topics_path):
        return topics

    for filename in os.listdir(ads_and_topics_path):
        file_path = os.path.join(ads_and_topics_path, filename)
        if filename.endswith(".json") and os.path.isfile(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if "impressions_history_recs_hidden_authors" in data:
                        for item in data["impressions_history_recs_hidden_authors"]:
                            if "string_map_data" in item and "Benutzername" in item["string_map_data"]:
                                topics.add(item["string_map_data"]["Benutzername"]["value"])
                    if "impressions_history_ads_seen" in data:
                        for item in data["impressions_history_ads_seen"]:
                            if "string_map_data" in item and "Time" in item["string_map_data"]:
                                topics.add("Ads seen at time: " + str(item["string_map_data"]["Time"]["timestamp"]))
                    if "impressions_history_posts_seen" in data:
                        for item in data["impressions_history_posts_seen"]:
                            if "string_map_data" in item and "Author" in item["string_map_data"]:
                                topics.add(item["string_map_data"]["Author"]["value"])
                    if "impressions_history_chaining_seen" in data:
                        for item in data["impressions_history_chaining_seen"]:
                            if "string_map_data" in item and "Username" in item["string_map_data"]:
                                topics.add(item["string_map_data"]["Username"]["value"])
                    if "impressions_history_videos_watched" in data:
                        for item in data["impressions_history_videos_watched"]:
                            if "string_map_data" in item and "Time" in item["string_map_data"]:
                                topics.add("Video watched at time: " + str(item["string_map_data"]["Time"]["timestamp"]))
            except (json.JSONDecodeError, KeyError) as e:
                raise ValueError(f"Error: Failed to parse JSON or missing keys in {filename}. {str(e)}")
    
    return topics

def write_to_csv(topics, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics:
            writer.writerow([topic])

try:
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    topics_of_interest = get_topics_of_interest(root_dir)
    write_to_csv(topics_of_interest, 'query_responses/results.csv')
except Exception as e:
    print(str(e))