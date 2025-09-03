import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Define the path to the your_topics.json file
        topics_path = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")
        
        # Check if the file exists
        if not os.path.exists(topics_path):
            print("Warning: The your_topics.json file does not exist. Returning an empty CSV.")
            return []
        
        # Read the JSON file
        with open(topics_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract the topics of interest
        topics = []
        if "topics_your_topics" in data:
            for topic in data["topics_your_topics"]:
                if "string_map_data" in topic and "Name" in topic["string_map_data"]:
                    topics.append(topic["string_map_data"]["Name"]["value"])
        
        return topics
    
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except json.JSONDecodeError:
        raise ValueError("Error: The your_topics.json file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {str(e)}")

def write_to_csv(topics, output_path):
    try:
        # Write the topics to a CSV file
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])  # Write the header
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to CSV: {str(e)}")

def main():
    try:
        # Get the topics of interest
        topics = get_topics_of_interest(root_dir)
        
        # Define the output CSV file path
        output_path = 'query_responses/results.csv'
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the topics to the CSV file
        write_to_csv(topics, output_path)
        
        print(f"Topics of interest have been written to {output_path}")
    
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()