import os
import json
import csv

# Variable referring to the file input
root_dir = "root_dir"

def main():
    # Define the path to the JSON file
    json_file_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")
    csv_file_path = "query_responses/results.csv"

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        # If the JSON file does not exist, create a CSV file with only the column headers
        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Topics of Interest"])
        return

    # Read the JSON file
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The JSON file is not properly formatted.")
    
    # Extract topics of interest
    topics_of_interest = []
    if "topics_your_topics" in data:
        for topic in data["topics_your_topics"]:
            if "string_map_data" in topic and "Name" in topic["string_map_data"]:
                topics_of_interest.append(topic["string_map_data"]["Name"]["value"])
    
    # Write the topics to a CSV file
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            csv_writer.writerow([topic])

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)