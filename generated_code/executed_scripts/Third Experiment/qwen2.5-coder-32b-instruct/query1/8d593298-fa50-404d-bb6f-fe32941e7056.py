import os
import csv
import json

root_dir = "root_dir"

def find_topics_of_interest(root_dir):
    topics_of_interest = []

    # Define the path to the file containing topics of interest
    topics_file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "other_categories_used_to_reach_you.json")

    try:
        # Check if the file exists
        if not os.path.exists(topics_file_path):
            raise FileNotFoundError(f"FileNotFoundError: The file {topics_file_path} does not exist.")

        # Open and read the JSON file
        with open(topics_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract topics of interest
        if 'label_values' in data:
            for label_value in data['label_values']:
                if 'label' in label_value:
                    topics_of_interest.append(label_value['label'])

    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file could not be decoded as JSON.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")

    return topics_of_interest

def save_to_csv(topics_of_interest):
    # Define the path to save the CSV file
    csv_file_path = 'query_responses/results.csv'

    # Ensure the directory exists
    os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

    # Write the topics of interest to a CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Topics of Interest'])
        for topic in topics_of_interest:
            writer.writerow([topic])

# Main execution
try:
    topics_of_interest = find_topics_of_interest(root_dir)
    save_to_csv(topics_of_interest)
except Exception as e:
    print(e)
    save_to_csv([])  # Save an empty CSV file with only the column headers if an error occurs