import os
import json
import csv

def extract_topics_of_interest(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    topics_of_interest = set()

    # Define the paths to the relevant JSON files
    ads_about_meta_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "ads_about_meta.json")
    ad_preferences_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "ad_preferences.json")

    # Function to extract topics from a JSON file
    def extract_topics_from_json(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if "label_values" in data:
                    for item in data["label_values"]:
                        if isinstance(item, dict) and "label" in item and "value" in item:
                            topics_of_interest.add(item["value"])
                        elif isinstance(item, dict) and "dict" in item:
                            for sub_item in item["dict"]:
                                if isinstance(sub_item, dict) and "label" in sub_item and "value" in sub_item:
                                    topics_of_interest.add(sub_item["value"])
        except FileNotFoundError:
            pass  # Ignore if the file is not found
        except json.JSONDecodeError:
            raise ValueError("Error: Invalid JSON format in file {}".format(file_path))

    # Extract topics from the relevant JSON files
    extract_topics_from_json(ads_about_meta_path)
    extract_topics_from_json(ad_preferences_path)

    # Write the results to a CSV file
    output_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

# Define the root directory
root_dir = "root_dir"

# Execute the function
extract_topics_of_interest(root_dir)