import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics_of_interest = []

    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        topics_path = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")

        if not os.path.exists(topics_path):
            return topics_of_interest

        with open(topics_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if "topics_your_topics" in data:
            for topic in data["topics_your_topics"]:
                if "string_map_data" in topic and "Name" in topic["string_map_data"]:
                    topics_of_interest.append(topic["string_map_data"]["Name"]["value"])

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

    return topics_of_interest

def write_to_csv(topics_of_interest):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

if __name__ == "__main__":
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest)
    except Exception as e:
        print(e)