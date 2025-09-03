import csv
import os

def get_topics_of_interest(root_dir):
    try:
        topics_of_interest = []
        for file in os.listdir(root_dir):
            if file.endswith(".json"):
                with open(os.path.join(root_dir, file), 'r') as f:
                    data = json.load(f)
                    if 'reels.json' in file:
                        for reel in data['reels.json']['structure']['ig_reels_media']:
                            for media in reel['media']:
                                for topic in media['interest_topics']:
                                    topics_of_interest.append(topic['topic_name'])
                    elif 'stories.json' in file:
                        for story in data['stories.json']['structure']['ig_stories']:
                            topics_of_interest.append('Stories')
        return topics_of_interest
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except json.JSONDecodeError as e:
        raise ValueError("ValueError: Unable to parse JSON file.")
    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the data.")

def write_to_csv(topics_of_interest):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        writer.writerows([[topic] for topic in topics_of_interest])

if __name__ == "__main__":
    root_dir = "root_dir"
    topics_of_interest = get_topics_of_interest(root_dir)
    write_to_csv(topics_of_interest)