import csv

# Input and output filenames
input_file = '../results/Final Experiment Prompt/error_log.csv'
output_file = '../results/Final Experiment Prompt/processed_error_log.csv'

# Keywords to look for in the message
file_not_found_keywords = [
    'FileNotFoundError',
    'file does not exist',
    'No such file or directory',
    'directory does not exist'
]

# Open the input and output CSV files
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
        open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()

    for row in reader:
        if row['Error Type'] == 'UnknownError':
            message = row['Message'].lower()
            if any(keyword.lower() in message for keyword in file_not_found_keywords):
                row['Error Type'] = 'FileNotFoundError'
        writer.writerow(row)

print(f"Processed CSV saved as '{output_file}'.")
