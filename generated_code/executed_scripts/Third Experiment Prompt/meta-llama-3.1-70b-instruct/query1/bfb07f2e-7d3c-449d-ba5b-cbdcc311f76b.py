import os
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize topics of interest
        topics_of_interest = []

        # Define the path to the recommended topics file
        recommended_topics_file = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

        # Check if the recommended topics file exists
        if os.path.exists(recommended_topics_file):
            # Open and read the recommended topics file
            with open(recommended_topics_file, 'r') as file:
                # Since the file structure is not provided, we assume it's a simple JSON file
                # with a list of topics
                import json
                data = json.load(file)
                for topic in data["topics_your_topics"]:
                    topics_of_interest.append(topic["string_map_data"]["Name"]["value"])

        return topics_of_interest

    except Exception as e:
        raise ValueError("Error: " + str(e))

def write_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_file = 'query_responses/results.csv'

        # Create the output directory if it does not exist
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the topics of interest to the CSV file
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_topics_to_csv(topics_of_interest)
    except FileNotFoundError as e:
        # If the root directory does not exist, create an empty CSV file
        output_file = 'query_responses/results.csv'
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
        print(e)
    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()