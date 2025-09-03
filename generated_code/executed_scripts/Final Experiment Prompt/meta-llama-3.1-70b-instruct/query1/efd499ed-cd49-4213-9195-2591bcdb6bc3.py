import json
import csv
import os

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Define the path to the JSON file
        json_file_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            # If the file does not exist, return a list with a single empty string
            return [""]

        # Open and load the JSON file
        with open(json_file_path, "r") as json_file:
            data = json.load(json_file)

        # Extract the topics of interest
        topics_of_interest = [topic["string_map_data"]["Name"]["value"] for topic in data["topics_your_topics"]]

        return topics_of_interest

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON file: {e}")
    except KeyError as e:
        raise ValueError(f"ValueError: Missing key in JSON file: {e}")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred: {e}")

def save_to_csv(topics_of_interest):
    try:
        # Define the path to the CSV file
        csv_file_path = "query_responses/results.csv"

        # Create the directory if it does not exist
        csv_dir = os.path.dirname(csv_file_path)
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)

        # Save the topics of interest to the CSV file
        with open(csv_file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while saving to CSV: {e}")

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        save_to_csv(topics_of_interest)
    except Exception as e:
        print(f"Error: {e}")
        # Save a CSV file with only the column headers if an error occurs
        with open("query_responses/results.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Topics of Interest"])

if __name__ == "__main__":
    main()