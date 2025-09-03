import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to extract topics of interest from the JSON file
def extract_topics_of_interest(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            topics = []
            for label_value in data.get('label_values', []):
                label = label_value.get('label')
                if label == 'Topics of Interest':
                    for value in label_value.get('vec', []):
                        topics.append(value.get('value'))
            return topics
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The specified JSON file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON file.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

# Function to generate the CSV file
def generate_csv(topics):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Topics of Interest']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for topic in topics:
                writer.writerow({'Topics of Interest': topic})
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

# Main function to process the directory and generate the CSV
def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        topics_of_interest_json_path = os.path.join(root_dir, 'personal_information', 'information_about_you', 'locations_of_interest.json')

        if not os.path.exists(topics_of_interest_json_path):
            # If the file does not exist, create a CSV with only the header
            generate_csv([])
            return

        topics = extract_topics_of_interest(topics_of_interest_json_path)
        generate_csv(topics)
    except Exception as e:
        print(e)

# Execute the main function
if __name__ == "__main__":
    main()