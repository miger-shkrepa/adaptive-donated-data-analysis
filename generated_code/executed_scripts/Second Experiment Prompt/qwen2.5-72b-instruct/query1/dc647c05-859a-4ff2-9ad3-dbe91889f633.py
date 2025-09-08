import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics_of_interest = []

    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        personal_info_path = os.path.join(root_dir, "personal_information", "information_about_you", "locations_of_interest.json")
        if not os.path.exists(personal_info_path):
            print("Warning: locations_of_interest.json not found. Returning empty topics.")
            return topics_of_interest

        with open(personal_info_path, 'r') as file:
            data = json.load(file)

        if "label_values" in data:
            for item in data["label_values"]:
                if "vec" in item and item["vec"]:
                    for vec_item in item["vec"]:
                        if "value" in vec_item:
                            topics_of_interest.append(vec_item["value"])

    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error in {personal_info_path}. Reason: {e}")
    except Exception as e:
        raise Exception(f"Error: Unexpected error occurred. Reason: {e}")

    return topics_of_interest

def write_to_csv(topics_of_interest):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: Failed to write to CSV. Reason: {e}")

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()