import re
import os
import subprocess
import csv
import time

CURRENT_EXPERIMENT = "First Experiment"
ERROR_LOG_FILE = f"../results/{CURRENT_EXPERIMENT}/error_log.csv"

def extract_code(response: str, output_file: str = "generated_code/extracted_code.py"):
    if not response:
        print("Error: No Python code found in the response.")
        return

    if response.startswith("import"):
        code = response
    else:
        # Try to match code block with ```python
        match = re.search(r'```python\n(.*?)\n```', response, re.DOTALL)
        if match:
            code = match.group(1)
        else:
            # Try to match code block with plain ```
            match = re.search(r'```\n(.*?)\n```', response, re.DOTALL)
            if match:
                code = match.group(1)
            else:
                print("Error: No Python code found in the response.")
                return

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(code)


def modify_root_dir(file_path, new_value):
    # Attempt to open and read the file
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return

    modified = False
    # Modify the line containing root_dir while preserving indentation
    for i, line in enumerate(lines):
        if 'root_dir =' in line:
            indentation = re.match(r'^\s*', line).group(0)
            lines[i] = f"{indentation}root_dir = '{new_value}'\n"
            modified = True
            break  # Exit the loop once the line is found and modified

    if not modified:
        print(f"Error: Line referring to root directory not found in {file_path}.")
        return

    # Write the modified lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Replaces the root_dir assignment with a placeholder value
def demodify_root_dir(script_content):
    return re.sub(r'(\broot_dir\s*=\s*)[\'"].+[\'"]', r'\1"root_dir"', script_content)

# Cleans error message by removing redundancy.
def clean_error_message(error_message: str):
    if not error_message:
        return None, None

    # Case 1: Handle traceback-like error format (e.g., "FileNotFoundError: FileNotFoundError: ...")
    match = re.match(r"^(\w+Error): (.+)$", error_message)
    if match:
        error_type, error_msg = match.groups()

        # If the message starts with the same error type, remove it
        if error_msg.startswith(error_type + ": "):
            error_msg = error_msg[len(error_type) + 2:]  # Remove redundant error type

        return error_type, error_msg

    # Case 2: Handle simple error format (e.g., "Error: FileNotFoundError: ...")
    match_simple = re.match(r"^Error: (\w+Error): (.+)$", error_message)
    if match_simple:
        error_type, error_msg = match_simple.groups()

        # Remove redundant error type if present in the message
        if error_msg.startswith(error_type + ": "):
            error_msg = error_msg[len(error_type) + 2:]

        return error_type, error_msg

    # If it doesn't match either format, return the error message as is
    return None, error_message

# Logs the extracted error type, message, and attempt number into a CSV file.
def log_error(experiment_id: str, model_name: str, error_type: str, error_msg: str, attempt_number: int):
    if not error_type or not error_msg:
        return  # Skip logging if no valid error

    log_exists = os.path.isfile(ERROR_LOG_FILE)

    with open(ERROR_LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header if the file is newly created
        if not log_exists:
            writer.writerow(["Experiment ID", "Model", "Attempt Number", "Error Type", "Message"])

        writer.writerow([experiment_id, model_name, attempt_number, error_type, error_msg])

# Runs a Python script and captures errors in the output.
def run_python_script(experiment_id, model_name, attempt_number, script_path):
    if not os.path.isfile(script_path):
        print(f"Error: {script_path} not found.")
        return "Error: Script file not found."  # Return an error message

    error_message = None  # Store the first detected error
    traceback_detected = False
    first_traceback_error = None

    code_exec_start_time = time.time()

    process = subprocess.Popen(
        ["python", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8"
    )

    for line in process.stdout:
        # print(line, end="")  # Print output in real time

        # Detect the start of the first traceback
        if "Traceback (most recent call last):" in line:
            if not traceback_detected:
                traceback_detected = True
                first_traceback_error = None  # Reset error tracking

        # If inside the first traceback, capture the final error line
        if traceback_detected and not first_traceback_error:
            if re.match(r'^\w+Error: ', line.strip()):
                first_traceback_error = line.strip()

        # If no traceback, look for "Error: " message
        elif "Error: " in line and error_message is None:
            error_message = line.strip()

    process.wait()

    code_exec_end_time = time.time()
    code_exec_time = round(code_exec_end_time - code_exec_start_time, 2)

    # Process and log the error
    captured_error = first_traceback_error if first_traceback_error else error_message
    error_type, error_msg = clean_error_message(captured_error)

    # Log the cleaned error if we have both the type and message
    if error_type and error_msg:
        log_error(experiment_id, model_name, error_type, error_msg, attempt_number)
    elif captured_error:  # Fallback case
        log_error(experiment_id, model_name, "UnknownError", captured_error, attempt_number)

    # Return the cleaned error message or raw one
    return {
        "error": f"{error_type}: {error_msg}" if error_type and error_msg else captured_error,
        "code_exec_time": code_exec_time
    }