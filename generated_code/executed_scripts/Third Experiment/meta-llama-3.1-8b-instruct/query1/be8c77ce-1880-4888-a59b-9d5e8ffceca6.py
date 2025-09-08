import csv
import os

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise e

    topics_of_interest = []

    for filename in os.listdir(root_dir):
        if filename == "liked_posts.json":
            with open(os.path.join(root_dir, filename), 'r') as f:
                data = f.read()
                try:
                    import json
                    json_data = json.loads(data)
                    for post in json_data['likes_media_likes']:
                        topics_of_interest.append(post['title'])
                except ValueError as e:
                    print(f"Error parsing JSON in {filename}: {e}")
        elif filename == "saved_posts.json":
            with open(os.path.join(root_dir, filename), 'r') as f:
                data = f.read()
                try:
                    import json
                    json_data = json.loads(data)
                    for post in json_data['saved_saved_media']:
                        topics_of_interest.append(post['title'])
                except ValueError as e:
                    print(f"Error parsing JSON in {filename}: {e}")

    return topics_of_interest

def write_to_csv(topics_of_interest):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

try:
    topics_of_interest = get_topics_of_interest(root_dir)
    write_to_csv(topics_of_interest)
except Exception as e:
    raise e