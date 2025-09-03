import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the path to the recommended_topics.json file
recommended_topics_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

# Define the path to the output CSV file
output_csv_path = "query_responses/results.csv"

# Function to extract topics of interest
def extract_topics_of_interest(file_path):
    topics_of_interest = []

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")

    # Read the JSON file
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

    # Extract topics of interest
    try:
        for topic in data.get("topics_your_topics", []):
            name_value = topic.get("string_map_data", {}).get("Name", {}).get("value", "")
            if name_value:
                topics_of_interest.append(name_value)
    except (TypeError, AttributeError) as e:
        raise ValueError(f"ValueError: Error processing JSON data - {str(e)}")

    return topics_of_interest

# Function to write topics of interest to a CSV file
def write_topics_to_csv(topics, output_path):
    try:
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])
    except IOError as e:
        raise IOError(f"IOError: Error writing to CSV file - {str(e)}")

# Main function to execute the script
def main():
    try:
        topics_of_interest = extract_topics_of_interest(recommended_topics_path)
        write_topics_to_csv(topics_of_interest, output_csv_path)
    except Exception as e:
        # If any error occurs, write only the column headers to the CSV file
        write_topics_to_csv([], output_csv_path)
        print(e)

if __name__ == "__main__":
    main()