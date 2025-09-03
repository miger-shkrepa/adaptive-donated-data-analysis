import os
import csv

root_dir = "root_dir"

def find_topics_of_interest(root_directory):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_directory):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Define the path to the topics file
        topics_file_path = os.path.join(root_directory, "preferences", "your_topics", "recommended_topics.json")
        
        # Check if the topics file exists
        if not os.path.exists(topics_file_path):
            raise FileNotFoundError("FileNotFoundError: The recommended_topics.json file does not exist.")
        
        # Read the topics file
        with open(topics_file_path, 'r') as file:
            import json
            data = json.load(file)
        
        # Extract topics of interest
        topics_of_interest = []
        for topic in data.get('topics_your_topics', []):
            string_map_data = topic.get('string_map_data', {})
            name_data = string_map_data.get('Name', {})
            value = name_data.get('value', '')
            if value:
                topics_of_interest.append(value)
        
        # Write the topics to a CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
            for topic in topics_of_interest:
                writer.writerow([topic])
    
    except FileNotFoundError as e:
        # Create a CSV file with only the column headers if the file is not found
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {str(e)}")

# Call the function with the root directory
find_topics_of_interest(root_dir)