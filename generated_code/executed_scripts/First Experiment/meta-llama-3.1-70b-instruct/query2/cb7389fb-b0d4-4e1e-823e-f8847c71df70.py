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
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                # Check if file is 'ads_viewed.json'
                if file == 'ads_viewed.json':
                    file_path = os.path.join(root, file)
                    # Open and load JSON file
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        # Iterate through impressions history
                        for impression in data['impressions_history_ads_seen']:
                            # Get company name (Author)
                            company_name = impression['string_map_data']['Author']['value']
                            # Increment number of ads viewed for company
                            if company_name in ads_viewed:
                                ads_viewed[company_name] += 1
                            else:
                                ads_viewed[company_name] = 1

        return ads_viewed

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")

    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON file - {e}")

    except Exception as e:
        raise ValueError(f"ValueError: An error occurred - {e}")

def save_to_csv(ads_viewed):
    try:
        # Create CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Company Name', 'Number of Ads Viewed']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write data
            for company, count in ads_viewed.items():
                writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})

    except Exception as e:
        raise ValueError(f"ValueError: Error saving to CSV file - {e}")

def main():
    try:
        ads_viewed = get_ads_viewed(root_dir)
        save_to_csv(ads_viewed)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()