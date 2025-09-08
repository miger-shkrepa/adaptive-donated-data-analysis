import os
import json
import csv

root_dir = "root_dir"

def get_ads_viewed(root_dir):
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the results
        ads_viewed = {}

        # Iterate over all files in the directory
        for dir_path, dir_names, file_names in os.walk(root_dir):
            for file_name in file_names:
                # Check if the file is a JSON file
                if file_name.endswith(".json"):
                    file_path = os.path.join(dir_path, file_name)
                    try:
                        # Open and load the JSON file
                        with open(file_path, 'r') as file:
                            data = json.load(file)

                        # Check if the file contains ads information
                        if "impressions_history_ads_seen" in data:
                            # Extract the ads information
                            for ad in data["impressions_history_ads_seen"]:
                                author = ad["string_map_data"]["Author"]["value"]
                                if author not in ads_viewed:
                                    ads_viewed[author] = 1
                                else:
                                    ads_viewed[author] += 1

                    except json.JSONDecodeError:
                        raise ValueError("ValueError: The file {} is not a valid JSON file.".format(file_path))

        return ads_viewed

    except Exception as e:
        raise Exception("Error: {}".format(str(e)))

def save_to_csv(ads_viewed):
    try:
        # Save the results to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, count in ads_viewed.items():
                writer.writerow([company, count])

    except Exception as e:
        raise Exception("Error: {}".format(str(e)))

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        save_to_csv(ads_viewed)
    except Exception as e:
        print("Error: {}".format(str(e)))

if __name__ == "__main__":
    main()