import os
import csv

root_dir = "root_dir"

def get_topics_of_interest(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize an empty list to store topics of interest
        topics_of_interest = []

        # Define the path to the 'your_topics' directory
        your_topics_dir = os.path.join(root_dir, 'preferences', 'your_topics')

        # Check if the 'your_topics' directory exists
        if os.path.exists(your_topics_dir):
            # Iterate over all files in the 'your_topics' directory
            for filename in os.listdir(your_topics_dir):
                # Check if the file is a JSON file
                if filename.endswith('.json'):
                    # Define the path to the JSON file
                    json_file_path = os.path.join(your_topics_dir, filename)

                    # Try to open and read the JSON file
                    try:
                        with open(json_file_path, 'r') as json_file:
                            # Since the JSON structure is not provided, we assume it's a simple list of topics
                            # If the structure is different, you'll need to adjust this part accordingly
                            topics_of_interest = [line.strip() for line in json_file.readlines()]
                    except Exception as e:
                        raise ValueError("ValueError: Failed to read the JSON file: " + str(e))

        # Return the list of topics of interest
        return topics_of_interest

    except Exception as e:
        raise Exception("Error: " + str(e))

def write_topics_to_csv(topics_of_interest):
    try:
        # Define the path to the output CSV file
        output_csv_path = 'query_responses/results.csv'

        # Create the 'query_responses' directory if it doesn't exist
        output_dir = os.path.dirname(output_csv_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Write the topics of interest to the CSV file
        with open(output_csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Topics of Interest'])  # Write the header
            for topic in topics_of_interest:
                csv_writer.writerow([topic])

    except Exception as e:
        raise Exception("Error: " + str(e))

def main():
    try:
        topics_of_interest = get_topics_of_interest(root_dir)
        write_topics_to_csv(topics_of_interest)
    except Exception as e:
        # If an error occurs, write an empty CSV file with only the header
        try:
            with open('query_responses/results.csv', 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Topics of Interest'])
        except Exception as e:
            raise Exception("Error: " + str(e))

if __name__ == "__main__":
    main()