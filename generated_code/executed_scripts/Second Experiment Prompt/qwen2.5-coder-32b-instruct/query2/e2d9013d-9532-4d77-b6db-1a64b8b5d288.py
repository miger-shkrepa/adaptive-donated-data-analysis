import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file
def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Function to get ads viewed data
def get_ads_viewed_data(root_dir):
    ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    if not os.path.exists(ads_viewed_path):
        return {}
    ads_viewed_data = read_json_file(ads_viewed_path)
    return ads_viewed_data.get("impressions_history_ads_seen", [])

# Function to get ads about meta data
def get_ads_about_meta_data(root_dir):
    ads_about_meta_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "ads_about_meta.json")
    if not os.path.exists(ads_about_meta_path):
        return {}
    ads_about_meta_data = read_json_file(ads_about_meta_path)
    return ads_about_meta_data.get("label_values", [])

# Function to aggregate ads data
def aggregate_ads_data(ads_viewed_data, ads_about_meta_data):
    company_ads_count = {}
    for ad in ads_viewed_data:
        author = ad.get("string_map_data", {}).get("Author", {}).get("value", "Unknown")
        company_ads_count[author] = company_ads_count.get(author, 0) + 1
    return company_ads_count

# Main function to process data and generate CSV
def main():
    try:
        # Get ads viewed data
        ads_viewed_data = get_ads_viewed_data(root_dir)
        
        # Get ads about meta data
        ads_about_meta_data = get_ads_about_meta_data(root_dir)
        
        # Aggregate ads data
        company_ads_count = aggregate_ads_data(ads_viewed_data, ads_about_meta_data)
        
        # Prepare CSV data
        csv_data = [["Company Name", "Number of Ads Viewed"]]
        for company, count in company_ads_count.items():
            csv_data.append([company, count])
        
        # Write CSV file
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(csv_data)
    
    except Exception as e:
        # Handle any exceptions and write only headers if error occurs
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Company Name", "Number of Ads Viewed"])
        print(f"Error: {e}")

# Execute the main function
if __name__ == "__main__":
    main()