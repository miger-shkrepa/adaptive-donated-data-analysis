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

        # Define the path to the locations_of_interest.json file
        locations_of_interest_path = os.path.join(root_dir, "information_about_you", "locations_of_interest.json")

        # Check if the locations_of_interest.json file exists
        if os.path.exists(locations_of_interest_path):
            # Open and read the locations_of_interest.json file
            with open(locations_of_interest_path, "r") as file:
                # Since we don't know the exact structure of the JSON file, we'll assume it's a list of labels
                # and try to extract the labels
                import json
                data = json.load(file)
                for label_value in data.get("label_values", []):
                    label = label_value.get("label")
                    if label:
                        topics_of_interest.append(label)

        # Return the topics of interest
        return topics_of_interest

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

def write_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_path = "query_responses/results.csv"

        # Create the output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the topics of interest to the CSV file
        with open(output_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
            for topic in topics_of_interest:
                writer.writerow([topic])

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the topics of interest
        topics_of_interest = get_topics_of_interest(root_dir)

        # Write the topics of interest to a CSV file
        write_topics_to_csv(topics_of_interest)

    except FileNotFoundError as e:
        # If the root directory does not exist, write a CSV file with only the column headers
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Topics of Interest"])
        print(e)
    except Exception as e:
        # Print the error message
        print("Error: " + str(e))

if __name__ == "__main__":
    main()