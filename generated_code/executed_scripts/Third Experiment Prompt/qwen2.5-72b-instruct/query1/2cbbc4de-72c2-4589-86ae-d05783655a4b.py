import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

def extract_topics_of_interest(root_dir):
    topics_of_interest = set()
    
    # Define the path to the relevant JSON file
    reels_json_path = os.path.join(root_dir, 'your_instagram_activity', 'subscriptions', 'reels.json')
    
    # Check if the file exists
    if not os.path.exists(reels_json_path):
        print("Warning: The file 'reels.json' does not exist. Returning an empty CSV file.")
        return topics_of_interest
    
    try:
        with open(reels_json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Extract topics of interest from the JSON structure
            if 'subscriptions_reels' in data:
                for item in data['subscriptions_reels']:
                    if 'string_map_data' in item and 'User Name' in item['string_map_data']:
                        topics_of_interest.add(item['string_map_data']['User Name']['value'])
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error in 'reels.json'. Reason: {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing 'reels.json'. Reason: {e}")
    
    return topics_of_interest

def write_to_csv(topics_of_interest):
    # Define the output CSV file path
    output_csv_path = 'query_responses/results.csv'
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])  # Write the header
            
            for topic in topics_of_interest:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to CSV. Reason: {e}")

def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    try:
        topics_of_interest = extract_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest)
        print(f"CSV file has been successfully created at 'query_responses/results.csv'.")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()