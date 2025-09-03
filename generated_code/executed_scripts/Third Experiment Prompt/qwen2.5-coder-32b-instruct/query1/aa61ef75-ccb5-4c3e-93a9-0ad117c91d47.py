import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the topics of interest file
topics_of_interest_path = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Function to read JSON file and extract topics of interest
def extract_topics_of_interest(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            topics = []
            for entry in data.get("topics_your_topics", []):
                topic_name = entry.get("string_map_data", {}).get("Name", {}).get("value", "")
                if topic_name:
                    topics.append(topic_name)
            return topics
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The topics of interest file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The topics of interest file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while reading the topics of interest file: {str(e)}")

# Function to write topics to CSV
def write_topics_to_csv(topics, output_path):
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to the CSV file: {str(e)}")

# Main function to execute the query
def main():
    try:
        # Check if the topics of interest file exists
        if not os.path.exists(topics_of_interest_path):
            # If the file does not exist, create an empty CSV with only the header
            write_topics_to_csv([], output_csv_path)
            print("Topics of interest file not found. Created an empty CSV with headers.")
            return

        # Extract topics of interest
        topics = extract_topics_of_interest(topics_of_interest_path)

        # Write topics to CSV
        write_topics_to_csv(topics, output_csv_path)
        print("Successfully extracted and wrote topics of interest to CSV.")

    except Exception as e:
        print(str(e))

# Execute the main function
if __name__ == "__main__":
    main()