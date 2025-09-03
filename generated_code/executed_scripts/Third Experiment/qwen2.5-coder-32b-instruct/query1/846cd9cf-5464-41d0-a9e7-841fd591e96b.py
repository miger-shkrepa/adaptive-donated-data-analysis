import os
import json
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Function to check if a file exists and is accessible
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")

# Function to read JSON data from a file
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to extract topics of interest from ads_viewed.json
def extract_topics_of_interest(root_dir):
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    
    # Check if the ads_viewed.json file exists
    check_file_exists(ads_viewed_path)
    
    # Read the JSON data from the file
    ads_viewed_data = read_json_file(ads_viewed_path)
    
    # Extract topics of interest (authors of the ads)
    topics_of_interest = set()
    for entry in ads_viewed_data.get("impressions_history_ads_seen", []):
        author = entry.get("string_map_data", {}).get("Author", {}).get("value")
        if author:
            topics_of_interest.add(author)
    
    return topics_of_interest

# Main function to execute the script
def main():
    try:
        # Extract topics of interest
        topics_of_interest = extract_topics_of_interest(root_dir)
        
        # Define the output file path
        output_file_path = 'query_responses/results.csv'
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        
        # Write the topics of interest to a CSV file
        with open(output_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    
    except FileNotFoundError as e:
        # Handle file not found errors
        print(e)
        # Create an empty CSV file with only the column headers
        with open('query_responses/results.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
    except Exception as e:
        # Handle other exceptions
        print(f"Error: {str(e)}")

# Execute the main function
if __name__ == "__main__":
    main()