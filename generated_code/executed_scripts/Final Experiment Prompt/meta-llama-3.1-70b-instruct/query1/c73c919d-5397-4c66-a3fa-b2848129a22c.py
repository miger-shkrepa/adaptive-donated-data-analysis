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
            # If the file does not exist, return a CSV file with only the column headers
            with open('query_responses/results.csv', 'w', newline='') as csvfile:
                fieldnames = ['Topics of Interest']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        # Load the JSON data
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Extract the topics of interest
        topics_of_interest = [topic["string_map_data"]["Name"]["value"] for topic in data["topics_your_topics"]]

        # Write the topics of interest to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Topics of Interest']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for topic in topics_of_interest:
                writer.writerow({'Topics of Interest': topic})

    except FileNotFoundError as e:
        raise FileNotFoundError(f"FileNotFoundError: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"ValueError: Error parsing JSON: {e}")
    except KeyError as e:
        raise ValueError(f"ValueError: Missing key in JSON: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")

get_topics_of_interest(root_dir)