import os
import json
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    topics_of_interest = []

    try:
        ads_and_topics_path = os.path.join(root_dir, "ads_information", "ads_and_topics")
        if not os.path.exists(ads_and_topics_path):
            raise FileNotFoundError("FileNotFoundError: The ads_and_topics directory does not exist.")

        other_categories_used_path = os.path.join(ads_and_topics_path, "other_categories_used_to_reach_you.json")
        if not os.path.exists(other_categories_used_path):
            print("Warning: The other_categories_used_to_reach_you.json file does not exist. Returning an empty list.")
            return topics_of_interest

        with open(other_categories_used_path, 'r') as file:
            data = json.load(file)

        label_values = data.get("label_values", [])
        for item in label_values:
            ent_field_name = item.get("ent_field_name")
            vec = item.get("vec", [])
            for value in vec:
                topics_of_interest.append(value.get("value"))

    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error: JSON decoding error - {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {e}")

    return topics_of_interest

def write_to_csv(topics_of_interest):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while writing to CSV - {e}")

if __name__ == "__main__":
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_to_csv(topics_of_interest)
    except Exception as e:
        print(e)