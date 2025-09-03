import os
import csv
import json

# Variable referring to the file input
root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics_of_interest = []

    # Define the path to the JSON file containing topics of interest
    topics_file_path = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")

    try:
        # Check if the file exists
        if not os.path.exists(topics_file_path):
            raise FileNotFoundError(f"FileNotFoundError: The file {topics_file_path} does not exist.")
        
        # Open and read the JSON file
        with open(topics_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract topics of interest
        if "topics_your_topics" in data:
            for topic in data["topics_your_topics"]:
                if "string_map_data" in topic and "Name" in topic["string_map_data"]:
                    topics_of_interest.append(topic["string_map_data"]["Name"]["value"])
    
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file could not be decoded as JSON.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")

    return topics_of_interest

def save_to_csv(topics_of_interest, output_path):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the topics to a CSV file
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to CSV - {str(e)}")

# Get topics of interest
topics_of_interest = get_topics_of_interest(root_dir)

# Save the topics to a CSV file
save_to_csv(topics_of_interest, 'query_responses/results.csv')