import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the recommended topics file
recommended_topics_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Function to read JSON file and extract topics
def read_recommended_topics(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            topics = []
            for topic in data.get("topics_your_topics", []):
                string_map_data = topic.get("string_map_data", {})
                name = string_map_data.get("Name", {}).get("value", "")
                if name:
                    topics.append(name)
            return topics
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The recommended topics file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The recommended topics file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while reading the recommended topics file: {e}")

# Function to write topics to CSV
def write_topics_to_csv(topics, file_path):
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to the CSV file: {e}")

# Main function to execute the query
def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check if the recommended topics file exists
        if not os.path.exists(recommended_topics_path):
            # If the file does not exist, create an empty CSV with only the header
            write_topics_to_csv([], output_csv_path)
            return
        
        # Read the recommended topics
        topics = read_recommended_topics(recommended_topics_path)
        
        # Write the topics to the CSV file
        write_topics_to_csv(topics, output_csv_path)
    
    except Exception as e:
        print(e)

# Execute the main function
if __name__ == "__main__":
    main()