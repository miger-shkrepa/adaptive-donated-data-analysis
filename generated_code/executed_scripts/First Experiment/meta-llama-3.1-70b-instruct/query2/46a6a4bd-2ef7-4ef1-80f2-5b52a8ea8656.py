import os
import json
import csv

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize dictionary to store company names and number of ads viewed
        ads_viewed = {}

        # Iterate through all files in the directory
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                # Check if file is a JSON file
                if file_name.endswith(".json"):
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        # Open and load JSON file
                        with open(file_path, 'r') as file:
                            data = json.load(file)

                        # Check if file contains ads information
                        if "impressions_history_ads_seen" in data:
                            # Iterate through ads viewed
                            for ad in data["impressions_history_ads_seen"]:
                                # Get company name (Author)
                                company_name = ad["string_map_data"]["Author"]["value"]

                                # Increment number of ads viewed for company
                                if company_name in ads_viewed:
                                    ads_viewed[company_name] += 1
                                else:
                                    ads_viewed[company_name] = 1

                    except json.JSONDecodeError:
                        raise ValueError("ValueError: Invalid JSON file.")

        return ads_viewed

    except Exception as e:
        raise Exception("Error: " + str(e))

def save_to_csv(ads_viewed):
    try:
        # Create CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])  # Header
            for company, count in ads_viewed.items():
                writer.writerow([company, count])

    except Exception as e:
        raise Exception("Error: " + str(e))

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        save_to_csv(ads_viewed)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()