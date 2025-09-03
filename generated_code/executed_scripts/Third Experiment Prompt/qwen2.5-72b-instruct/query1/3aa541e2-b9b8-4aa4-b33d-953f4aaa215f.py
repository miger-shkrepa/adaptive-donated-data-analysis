import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Define the path to the your_topics.json file
        your_topics_path = os.path.join(root_dir, "preferences", "your_topics", "your_topics.json")
        
        # Check if the file exists
        if not os.path.exists(your_topics_path):
            raise FileNotFoundError("FileNotFoundError: The your_topics.json file does not exist.")
        
        # Read the JSON file
        with open(your_topics_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extract the topics of interest
        topics = []
        for item in data.get("topics_your_topics", []):
            topic_name = item.get("string_map_data", {}).get("Name", {}).get("value")
            if topic_name:
                topics.append(topic_name)
        
        return topics
    
    except FileNotFoundError as e:
        print(e)
        return []
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

def write_to_csv(topics, output_path):
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the topics to a CSV file
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

def main():
    try:
        # Get the topics of interest
        topics = get_topics_of_interest(root_dir)
        
        # Define the output CSV file path
        output_path = 'query_responses/results.csv'
        
        # Write the topics to a CSV file
        write_to_csv(topics, output_path)
        
        print(f"Topics of interest have been written to {output_path}")
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()