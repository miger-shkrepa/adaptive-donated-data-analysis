import os
import json
import csv

root_dir = "root_dir"

def get_interest_topics(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        topics_of_interest = set()
        
        # Path to the reels.json file
        reels_json_path = os.path.join(root_dir, "activity", "reels.json")
        
        if os.path.exists(reels_json_path):
            with open(reels_json_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                reels_media = data.get("ig_reels_media", [])
                for reel in reels_media:
                    media_list = reel.get("media", [])
                    for media in media_list:
                        interest_topics = media.get("interest_topics", [])
                        for topic in interest_topics:
                            topic_name = topic.get("topic_name")
                            if topic_name:
                                topics_of_interest.add(topic_name)
        else:
            print("Warning: reels.json does not exist. No topics of interest found.")
        
        # Save the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

# Call the function with the root directory
get_interest_topics(root_dir)