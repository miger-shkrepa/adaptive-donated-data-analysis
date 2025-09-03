import os
import csv
import json

root_dir = "root_dir"

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

def extract_topics_of_interest(root_dir):
    topics_of_interest = set()

    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

    if os.path.exists(ads_viewed_path):
        ads_viewed_data = read_json_file(ads_viewed_path)
        for entry in ads_viewed_data.get("impressions_history_ads_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                topics_of_interest.add(author)

    if os.path.exists(posts_viewed_path):
        posts_viewed_data = read_json_file(posts_viewed_path)
        for entry in posts_viewed_data.get("impressions_history_posts_seen", []):
            author = entry.get("string_map_data", {}).get("Author", {}).get("value")
            if author:
                topics_of_interest.add(author)

    return topics_of_interest

def save_topics_to_csv(topics_of_interest):
    try:
        os.makedirs(os.path.dirname('query_responses/results.csv'), exist_ok=True)
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: Failed to save the CSV file. {str(e)}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    topics_of_interest = extract_topics_of_interest(root_dir)
    save_topics_to_csv(topics_of_interest)

if __name__ == "__main__":
    main()