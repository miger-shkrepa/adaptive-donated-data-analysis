import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the JSON file of interest
        json_file_path = os.path.join(root_dir, 'ads_information', 'instagram_ads_and_businesses', 'other_categories_used_to_reach_you.json')

        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            print("Warning: The JSON file does not exist. Returning an empty CSV file.")
            return []

        # Read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Extract the topics of interest
        topics = []
        for label_value in data.get('label_values', []):
            for vec in label_value.get('vec', []):
                topics.append(vec.get('value'))

        return topics

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(topics, output_csv):
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_csv), exist_ok=True)

        # Write the topics to the CSV file
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])  # Write the header
            for topic in topics:
                writer.writerow([topic])

    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to CSV - {e}")

# Main execution
if __name__ == "__main__":
    try:
        topics = get_topics_of_interest(root_dir)
        write_to_csv(topics, output_csv)
        print(f"CSV file has been created at {output_csv}")
    except Exception as e:
        print(e)