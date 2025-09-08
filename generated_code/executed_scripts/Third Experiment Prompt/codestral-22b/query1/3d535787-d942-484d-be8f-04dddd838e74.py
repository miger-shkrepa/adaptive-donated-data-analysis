import os
import json
import csv

root_dir = "root_dir"
output_file = "query_responses/results.csv"

def get_topics_of_interest(root_dir):
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    topics_of_interest = []
    file_path = os.path.join(root_dir, "personal_information", "information_about_you", "locations_of_interest.json")

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            if "label_values" in data:
                for item in data["label_values"]:
                    if "vec" in item:
                        for vec_item in item["vec"]:
                            if "value" in vec_item:
                                topics_of_interest.append(vec_item["value"])

    return topics_of_interest

def save_to_csv(topics_of_interest, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Topics of Interest"])
        for topic in topics_of_interest:
            writer.writerow([topic])

try:
    topics_of_interest = get_topics_of_interest(root_dir)
    save_to_csv(topics_of_interest, output_file)
except Exception as e:
    print(f"Error: {str(e)}")