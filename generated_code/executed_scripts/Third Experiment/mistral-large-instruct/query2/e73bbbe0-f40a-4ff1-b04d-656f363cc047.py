import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to process the JSON files and extract the required information
def process_ads_information(root_dir):
    ads_info = {}

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    # Define the paths to the JSON files
    posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')
    videos_watched_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'videos_watched.json')
    subscription_for_no_ads_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'subscription_for_no_ads.json')

    # Process posts_viewed.json
    if os.path.exists(posts_viewed_path):
        with open(posts_viewed_path, 'r') as file:
            data = json.load(file)
            for post in data.get('impressions_history_posts_seen', []):
                author = post.get('string_map_data', {}).get('Author', {}).get('value', '')
                if author not in ads_info:
                    ads_info[author] = 0
                ads_info[author] += 1

    # Process videos_watched.json
    if os.path.exists(videos_watched_path):
        with open(videos_watched_path, 'r') as file:
            data = json.load(file)
            for video in data.get('impressions_history_videos_watched', []):
                author = video.get('string_map_data', {}).get('Author', {}).get('value', '')
                if author not in ads_info:
                    ads_info[author] = 0
                ads_info[author] += 1

    # Process subscription_for_no_ads.json
    if os.path.exists(subscription_for_no_ads_path):
        with open(subscription_for_no_ads_path, 'r') as file:
            data = json.load(file)
            for label in data.get('label_values', []):
                company = label.get('label', '')
                if company not in ads_info:
                    ads_info[company] = 0
                ads_info[company] += 1

    return ads_info

# Function to write the results to a CSV file
def write_to_csv(ads_info, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company, count in ads_info.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

# Main function to execute the script
def main():
    try:
        ads_info = process_ads_information(root_dir)
        write_to_csv(ads_info, output_csv)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()