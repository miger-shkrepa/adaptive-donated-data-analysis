import os
import json
import csv

def extract_topics_of_interest(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    topics_of_interest = []

    # Define the path to the locations_of_interest.json file
    locations_of_interest_path = os.path.join(root_dir, "information_about_you", "locations_of_interest.json")

    # Check if the file exists
    if os.path.exists(locations_of_interest_path):
        try:
            with open(locations_of_interest_path, 'r') as file:
                data = json.load(file)
                for item in data.get("label_values", []):
                    if "label" in item and "vec" in item:
                        for vec_item in item["vec"]:
                            if "value" in vec_item:
                                topics_of_interest.append(vec_item["value"])
        except json.JSONDecodeError:
            raise ValueError("Error: Failed to decode JSON from locations_of_interest.json.")
        except Exception as e:
            raise ValueError(f"Error: An unexpected error occurred while processing locations_of_interest.json. {str(e)}")

    # Define the path to save the CSV file
    output_csv_path = 'query_responses/results.csv'

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    # Write the results to a CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['Topics of Interest']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for topic in topics_of_interest:
            writer.writerow({'Topics of Interest': topic})

if __name__ == "__main__":
    root_dir = "root_dir"
    extract_topics_of_interest(root_dir)