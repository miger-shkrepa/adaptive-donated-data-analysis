import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

def find_topics_of_interest(root_dir):
    topics_of_interest = []

    # Define the path to the JSON file containing topics of interest
    topics_file_path = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")

    try:
        # Check if the file exists
        if not os.path.exists(topics_file_path):
            raise FileNotFoundError(f"FileNotFoundError: The file {topics_file_path} does not exist.")
        
        # Read the JSON file
        with open(topics_file_path, 'r', encoding='utf-8') as file:
            import json
            data = json.load(file)
        
        # Extract topics of interest
        if "topics_your_topics" in data:
            for topic in data["topics_your_topics"]:
                if "string_map_data" in topic and "Name" in topic["string_map_data"]:
                    topics_of_interest.append(topic["string_map_data"]["Name"]["value"])
    
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"ValueError: The file {topics_file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"Error: An unexpected error occurred while processing the file {topics_file_path}: {e}")

    return topics_of_interest

def save_to_csv(topics_of_interest, output_path):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write to CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    
    except Exception as e:
        print(f"Error: An unexpected error occurred while writing to the CSV file: {e}")

# Find topics of interest
topics_of_interest = find_topics_of_interest(root_dir)

# Save the results to a CSV file
save_to_csv(topics_of_interest, 'query_responses/results.csv')