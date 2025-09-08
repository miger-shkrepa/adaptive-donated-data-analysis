import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and handle errors
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to process the data and generate the CSV
def generate_ads_viewed_csv(root_dir):
    # Define the path to the results CSV
    results_csv_path = 'query_responses/results.csv'
    
    # Ensure the directory for the results CSV exists
    os.makedirs(os.path.dirname(results_csv_path), exist_ok=True)
    
    # Initialize the CSV writer
    with open(results_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
    
    # Check if the required directory structure exists
    ads_data_path = os.path.join(root_dir, 'your_instagram_activity', 'ads')
    if not os.path.exists(ads_data_path):
        return
    
    # Check if the required JSON file exists
    ads_json_path = os.path.join(ads_data_path, 'ads_data.json')
    if not os.path.exists(ads_json_path):
        return
    
    # Read the JSON file
    ads_data = read_json_file(ads_json_path)
    
    # Process the ads data and write to CSV
    with open(results_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        for ad in ads_data.get('ads', []):
            company_name = ad.get('company_name', 'Unknown')
            ads_viewed = ad.get('ads_viewed', 0)
            csvwriter.writerow([company_name, ads_viewed])

# Main function to handle the script execution
def main():
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        # Generate the CSV file
        generate_ads_viewed_csv(root_dir)
    
    except (FileNotFoundError, ValueError) as e:
        print(e)
        # Ensure the CSV file with headers is created even if there's an error
        results_csv_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(results_csv_path), exist_ok=True)
        with open(results_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])

# Execute the main function
if __name__ == "__main__":
    main()