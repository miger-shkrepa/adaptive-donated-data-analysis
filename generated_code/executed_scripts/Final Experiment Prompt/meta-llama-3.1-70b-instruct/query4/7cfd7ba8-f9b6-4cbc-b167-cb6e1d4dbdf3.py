import json
import csv
import os

root_dir = "root_dir"

def get_company_names(root_dir):
    """
    Extracts company names from the advertisers_using_your_activity_or_information.json file.

    Args:
        root_dir (str): The path to the root directory.

    Returns:
        list: A list of company names.
    """
    company_names = []
    file_path = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses", "advertisers_using_your_activity_or_information.json")

    if os.path.exists(root_dir):
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
                    for entry in data.get("ig_custom_audiences_all_types", []):
                        company_names.append(entry.get("advertiser_name", ""))
            except json.JSONDecodeError:
                raise ValueError("Error: The file advertisers_using_your_activity_or_information.json is not a valid JSON file.")
        else:
            # If the file does not exist, return an empty list without printing an error message
            pass
    else:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    return company_names

def save_to_csv(company_names):
    """
    Saves the company names to a CSV file.

    Args:
        company_names (list): A list of company names.
    """
    with open("query_responses/results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name"])
        for company_name in company_names:
            writer.writerow([company_name])

def main():
    try:
        company_names = get_company_names(root_dir)
        save_to_csv(company_names)
    except FileNotFoundError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
        print(f"Error: {e}")
    except ValueError as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
        print(f"Error: {e}")
    except Exception as e:
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name"])
        print(f"Error: {e}")

if __name__ == "__main__":
    main()