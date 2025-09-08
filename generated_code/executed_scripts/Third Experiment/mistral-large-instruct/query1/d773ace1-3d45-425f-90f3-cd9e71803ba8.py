import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract topics of interest from the ads_viewed.json file
def extract_topics_of_interest(root_dir):
    topics_of_interest = set()

    # Define the path to the ads_viewed.json file
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")

    # Check if the ads_viewed.json file exists
    if not os.path.exists(ads_viewed_path):
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")

    # Read the ads_viewed.json file
    try:
        with open(ads_viewed_path, 'r') as file:
            ads_viewed_data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON.")

    # Extract topics of interest from the ads_viewed data
    for ad in ads_viewed_data.get("impressions_history_ads_seen", []):
        for key, value in ad.get("string_map_data", {}).items():
            if key == "Author":
                topics_of_interest.add(value.get("value", ""))

    return topics_of_interest

# Function to save the topics of interest to a CSV file
def save_topics_to_csv(topics_of_interest):
    output_path = 'query_responses/results.csv'

    # Create the output directory if it does not exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the topics of interest to the CSV file
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

# Main function to execute the script
def main():
    try:
        topics_of_interest = extract_topics_of_interest(root_dir)
        save_topics_to_csv(topics_of_interest)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()