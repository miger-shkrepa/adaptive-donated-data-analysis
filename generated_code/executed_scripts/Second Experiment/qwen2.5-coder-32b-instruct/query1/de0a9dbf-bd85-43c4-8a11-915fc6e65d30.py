import os
import csv

root_dir = "root_dir"

def find_topics_of_interest(root_dir):
    topics_of_interest = []

    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Construct the path to the locations_of_interest.json file
        locations_of_interest_path = os.path.join(root_dir, "information_about_you", "locations_of_interest.json")

        # Check if the locations_of_interest.json file exists
        if os.path.exists(locations_of_interest_path):
            with open(locations_of_interest_path, 'r', encoding='utf-8') as file:
                import json
                data = json.load(file)

                # Extract topics of interest from the label_values
                for item in data.get('label_values', []):
                    if 'label' in item:
                        topics_of_interest.append(item['label'])
        else:
            print("Warning: locations_of_interest.json not found. Continuing without it.")

    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return topics_of_interest

def save_to_csv(topics_of_interest):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname('query_responses/results.csv'), exist_ok=True)

        # Write the topics of interest to a CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        print(f"An error occurred while writing to the CSV file: {e}")

# Find topics of interest and save them to a CSV file
topics_of_interest = find_topics_of_interest(root_dir)
save_to_csv(topics_of_interest)