import os
import csv

# The root directory of the data package
root_dir = "root_dir"

# Function to find and parse the topics of interest from the stories.json file
def find_topics_of_interest(root_dir):
    # Define the path to the stories.json file
    stories_json_path = os.path.join(root_dir, "personal_information", "device_information", "stories.json")
    
    # Check if the stories.json file exists
    if not os.path.exists(stories_json_path):
        raise FileNotFoundError("FileNotFoundError: The stories.json file does not exist.")
    
    # Initialize a set to store unique topics of interest
    topics_of_interest = set()
    
    # Open and read the stories.json file
    try:
        with open(stories_json_path, 'r') as file:
            import json
            stories_data = json.load(file)
            
            # Check if the structure contains the expected keys
            if 'structure' not in stories_data or 'ig_stories' not in stories_data['structure']:
                raise ValueError("ValueError: The stories.json file does not contain the expected structure.")
            
            # Iterate through each story to find topics of interest
            for story in stories_data['structure']['ig_stories']:
                if 'interest_topics' in story:
                    for topic in story['interest_topics']:
                        if 'topic_name' in topic:
                            topics_of_interest.add(topic['topic_name'])
    
    except json.JSONDecodeError:
        raise ValueError("ValueError: The stories.json file is not a valid JSON file.")
    
    return topics_of_interest

# Main function to execute the script
def main():
    try:
        # Find topics of interest
        topics = find_topics_of_interest(root_dir)
        
        # Define the path for the output CSV file
        output_csv_path = 'query_responses/results.csv'
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        
        # Write the topics to a CSV file
        with open(output_csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])  # Write the header
            for topic in topics:
                writer.writerow([topic])  # Write each topic as a row
    
    except (FileNotFoundError, ValueError) as e:
        # Handle exceptions by writing only the column headers to the CSV file
        output_csv_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        with open(output_csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Topics of Interest'])  # Write the header

# Execute the main function
if __name__ == "__main__":
    main()