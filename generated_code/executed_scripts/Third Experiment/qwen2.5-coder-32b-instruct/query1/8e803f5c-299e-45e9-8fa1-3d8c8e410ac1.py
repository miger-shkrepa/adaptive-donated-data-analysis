import os
import csv
import json

root_dir = "root_dir"

def find_topics_of_interest(root_dir):
    topics_of_interest = set()

    # Define the path to the ad preferences file
    ad_preferences_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "ad_preferences.json")

    # Check if the ad preferences file exists
    if not os.path.exists(ad_preferences_path):
        return topics_of_interest

    try:
        # Open and load the ad preferences file
        with open(ad_preferences_path, 'r', encoding='utf-8') as file:
            ad_preferences_data = json.load(file)

        # Extract topics of interest from the ad preferences data
        if 'label_values' in ad_preferences_data:
            for item in ad_preferences_data['label_values']:
                if 'dict' in item:
                    for sub_item in item['dict']:
                        if 'label' in sub_item:
                            topics_of_interest.add(sub_item['label'])

    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ad preferences file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ad preferences file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the ad preferences file: {str(e)}")

    return topics_of_interest

def main():
    try:
        # Find topics of interest
        topics_of_interest = find_topics_of_interest(root_dir)

        # Define the output CSV file path
        output_csv_path = 'query_responses/results.csv'

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

        # Write the topics of interest to the CSV file
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()