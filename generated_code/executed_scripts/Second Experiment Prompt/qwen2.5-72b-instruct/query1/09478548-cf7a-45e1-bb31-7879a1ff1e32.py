import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics_of_interest = []

    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Path to the JSON file containing topics of interest
        topics_file_path = os.path.join(root_dir, "personal_information", "information_about_you", "locations_of_interest.json")

        if not os.path.exists(topics_file_path):
            print("Warning: The file 'locations_of_interest.json' does not exist. Returning an empty list.")
            return topics_of_interest

        with open(topics_file_path, 'r') as file:
            data = json.load(file)

        # Extract topics of interest from the JSON structure
        for label_value in data.get("label_values", []):
            if "vec" in label_value:
                for value in label_value["vec"]:
                    topics_of_interest.append(value["value"])

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

    return topics_of_interest

def write_to_csv(topics_of_interest):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])  # Write the header

            for topic in topics_of_interest:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An error occurred while writing to CSV - {e}")

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()