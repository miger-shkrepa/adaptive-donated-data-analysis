import os
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON files
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return eval(file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except Exception as e:
        raise ValueError(f"ValueError: Error reading the file {file_path}: {str(e)}")

# Function to extract topics of interest
def extract_topics_of_interest(root_dir):
    topics_of_interest = []

    # Define the path to the recommended topics file
    topics_file_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

    # Check if the file exists
    if not os.path.exists(topics_file_path):
        return topics_of_interest

    # Read the JSON file
    try:
        topics_data = read_json_file(topics_file_path)
    except Exception as e:
        print(f"Error: {str(e)}")
        return topics_of_interest

    # Extract topics
    if "topics_your_topics" in topics_data:
        for topic in topics_data["topics_your_topics"]:
            if "string_map_data" in topic and "Name" in topic["string_map_data"]:
                topics_of_interest.append(topic["string_map_data"]["Name"]["value"])

    return topics_of_interest

# Main function to execute the query
def main():
    # Extract topics of interest
    topics_of_interest = extract_topics_of_interest(root_dir)

    # Define the output CSV file path
    output_csv_path = "query_responses/results.csv"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Write the results to a CSV file
    try:
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                csv_writer.writerow([topic])
    except Exception as e:
        raise ValueError(f"ValueError: Error writing to the CSV file {output_csv_path}: {str(e)}")

# Execute the main function
if __name__ == "__main__":
    main()