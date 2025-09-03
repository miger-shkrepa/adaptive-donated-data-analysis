import os
import csv
import json

root_dir = "root_dir"

def extract_interest_topics(root_dir):
    topics_of_interest = set()
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        reels_json_path = os.path.join(root_dir, "personal_information", "device_information", "reels.json")
        if not os.path.exists(reels_json_path):
            print("Warning: reels.json does not exist. Proceeding without its data.")
        else:
            with open(reels_json_path, 'r') as file:
                reels_data = json.load(file)
                for reel in reels_data.get("ig_reels_media", []):
                    for media in reel.get("media", []):
                        for topic in media.get("interest_topics", []):
                            topics_of_interest.add(topic.get("topic_name", ""))
        
        stories_json_path = os.path.join(root_dir, "personal_information", "device_information", "stories.json")
        if not os.path.exists(stories_json_path):
            print("Warning: stories.json does not exist. Proceeding without its data.")
        else:
            with open(stories_json_path, 'r') as file:
                stories_data = json.load(file)
                for story in stories_data.get("ig_stories", []):
                    if "interest_topics" in story:
                        for topic in story.get("interest_topics", []):
                            topics_of_interest.add(topic.get("topic_name", ""))
        
        if not topics_of_interest:
            print("No topics of interest found.")
        
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

extract_interest_topics(root_dir)