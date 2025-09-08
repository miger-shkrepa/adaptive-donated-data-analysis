import os
import json
import csv

# Variable referring to the file input
root_dir = "root_dir"

def main():
    # Define the path to the JSON file
    json_file_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
    output_csv_path = "query_responses/results.csv"

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    
    # Check if the JSON file exists
    if not os.path.exists(json_file_path):
        # If the JSON file does not exist, create an empty CSV with headers
        with open(output_csv_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
        return

    # Initialize a dictionary to count ads viewed by each company
    company_ads_count = {}

    try:
        # Open and read the JSON file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

            # Check if the required key exists in the JSON data
            if "impressions_history_ads_seen" not in data:
                raise ValueError("ValueError: The required key 'impressions_history_ads_seen' is missing in the JSON data.")

            # Iterate through each entry in the impressions_history_ads_seen list
            for entry in data["impressions_history_ads_seen"]:
                # Check if the required keys exist in the entry
                if "string_map_data" in entry and "Author" in entry["string_map_data"] and "value" in entry["string_map_data"]["Author"]:
                    # Extract the company name
                    company_name = entry["string_map_data"]["Author"]["value"]

                    # Increment the count for the company
                    if company_name in company_ads_count:
                        company_ads_count[company_name] += 1
                    else:
                        company_ads_count[company_name] = 1

    except json.JSONDecodeError:
        raise ValueError("ValueError: The JSON file is not properly formatted.")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Write the results to a CSV file
    with open(output_csv_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
        for company, count in company_ads_count.items():
            writer.writerow([company, count])

if __name__ == "__main__":
    main()