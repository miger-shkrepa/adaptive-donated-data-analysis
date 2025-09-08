import os
import csv
import json

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics_of_interest = set()

    # Check if the ads_viewed.json file exists and extract topics
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    if os.path.exists(ads_viewed_path):
        with open(ads_viewed_path, 'r', encoding='utf-8') as file:
            ads_viewed_data = json.load(file)
            for ad in ads_viewed_data.get("impressions_history_ads_seen", []):
                # Assuming the ad title or some other field indicates the topic
                # Here we use a placeholder since the actual structure is not detailed
                topics_of_interest.add("Ad Topic Placeholder")

    # Check if the posts_viewed.json file exists and extract topics
    posts_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")
    if os.path.exists(posts_viewed_path):
        with open(posts_viewed_path, 'r', encoding='utf-8') as file:
            posts_viewed_data = json.load(file)
            for post in posts_viewed_data.get("impressions_history_posts_seen", []):
                # Assuming the post author or some other field indicates the topic
                # Here we use a placeholder since the actual structure is not detailed
                topics_of_interest.add("Post Topic Placeholder")

    return topics_of_interest

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    topics_of_interest = get_topics_of_interest(root_dir)

    # Ensure the output directory exists
    output_dir = os.path.dirname('query_responses/results.csv')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write the topics to a CSV file
    with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

if __name__ == "__main__":
    main()