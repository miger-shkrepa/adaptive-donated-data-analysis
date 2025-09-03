import csv
import re
from collections import defaultdict, Counter

input_file = '../results/Final Experiment Prompt/processed_error_log.csv'
output_file = '../results/Final Experiment Prompt/error_log2.csv'

def extract_keywords(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

# Regex pattern to detect KeyError pattern like "Error: Error: 'some_word'"
keyerror_pattern = re.compile(r"Error: Error: '\w+'", re.IGNORECASE)

# Phrase for InvalidTimeStampFormat error (case insensitive)
invalid_timestamp_phrase = "invalid timestamp format"

# Phrase for UnicodeEncodeError detection (case insensitive)
unicode_encode_phrase = "'charmap' codec"

# Step 1: Collect messages by error type (excluding UnknownError)
error_keywords = defaultdict(Counter)
all_rows = []

with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames

    for row in reader:
        all_rows.append(row)
        error_type = row['Error Type']
        message = row['Message']
        if error_type != 'UnknownError':
            keywords = extract_keywords(message)
            error_keywords[error_type].update(keywords)

# Step 2: Build keyword sets for each known error type
error_type_templates = {
    err_type: set([kw for kw, count in counter.items() if count >= 2])
    for err_type, counter in error_keywords.items()
}

# Step 3: Reclassify UnknownError rows, apply custom rules first
for row in all_rows:
    message = row['Message'].lower()

    # Rule 1: KeyError pattern
    if keyerror_pattern.search(message):
        row['Error Type'] = 'KeyError'
        continue

    # Rule 2: Invalid timestamp format phrase
    if invalid_timestamp_phrase in message:
        row['Error Type'] = 'InvalidTimeStampFormat'
        continue

    # Rule 3: UnicodeEncodeError phrase
    if unicode_encode_phrase in message:
        row['Error Type'] = 'UnicodeEncodeError'

    if "no story engagement data found" in message:
        row['Error Type'] = 'DataNotFoundError'

    # Step 4: Existing enhanced classification for UnknownError
    if row['Error Type'] == 'UnknownError':
        message_keywords = extract_keywords(message)
        best_match = None
        max_overlap = 0

        for err_type, keywords in error_type_templates.items():
            overlap = len(message_keywords & keywords)
            if overlap > max_overlap:
                max_overlap = overlap
                best_match = err_type

        if best_match and max_overlap > 2:
            row['Error Type'] = best_match

# Step 5: Write output
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_rows)

print(f"Processed CSV with extended custom rules saved as '{output_file}'.")
