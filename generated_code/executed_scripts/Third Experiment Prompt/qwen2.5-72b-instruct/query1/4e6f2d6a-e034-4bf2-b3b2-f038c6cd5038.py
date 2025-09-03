import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        topics_of_interest = []

        # Construct the path to the topics file
        topics_file_path = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")

        # Check if the file exists
        if not os.path.exists(topics_file_path):
            print("Warning: The topics file does not exist. Returning an empty list.")
            return topics_of_interest

        # Read the JSON file
        with open(topics_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract the topics of interest
        if "topics_your_topics" in data:
            for topic in data["topics_your_topics"]:
                if "string_map_data" in topic and "Name" in topic["string_map_data"]:
                    topics_of_interest.append(topic["string_map_data"]["Name"]["value"])

        return topics_of_interest

    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: Failed to decode JSON data.")
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def write_to_csv(topics_of_interest):
    try:
        # Define the output file path
        output_file_path = 'query_responses/results.csv'

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        # Write the topics of interest to a CSV file
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])  # Write the header

            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest)
        print("CSV file has been created successfully.")
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()