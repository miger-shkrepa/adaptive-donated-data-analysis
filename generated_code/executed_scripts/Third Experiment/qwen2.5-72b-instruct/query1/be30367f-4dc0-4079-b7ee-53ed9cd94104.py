import os
import csv
import json

root_dir = "root_dir"

def get_topics_of_interest(root):
    topics = []
    try:
        if not os.path.exists(root):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Check if the required directory exists
        interests_path = os.path.join(root, "interests")
        if not os.path.exists(interests_path):
            return topics  # Return an empty list if the interests directory is not found

        # Iterate through the interests directory to find relevant JSON files
        for filename in os.listdir(interests_path):
            if filename.endswith(".json"):
                file_path = os.path.join(interests_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    # Assuming the JSON structure contains a list of topics under a key like 'topics'
                    if 'topics' in data:
                        topics.extend(data['topics'])
                    else:
                        raise ValueError("Error: JSON file does not contain 'topics' key.")
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
    
    return topics

def write_to_csv(topics):
    try:
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics:
                writer.writerow([topic])
    except Exception as e:
        print(f"Error: Failed to write to CSV file: {e}")

# Get topics of interest
topics_of_interest = get_topics_of_interest(root_dir)

# Write the topics to a CSV file
write_to_csv(topics_of_interest)