import os
import re
import time

def write_requests_total(directory_path, output_file_path):
    try:
        # Ensure the output directory exists, create it if not
        output_directory = os.path.dirname(output_file_path)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Store the last read position for each file
        last_positions = {}

        while True:
            # List all files in the specified directory that match the pattern "requests_log-*.txt"
            files = [f for f in os.listdir(directory_path) if f.startswith("requests_log-") and f.endswith(".txt")]

            # Initialize total
            total_requests = 0

            # Iterate through each file
            for file_name in files:
                file_path = os.path.join(directory_path, file_name)

                # Get the last read position for the file
                last_position = last_positions.get(file_name, 0)

                # Read and extract the numeric value after "Requests per second:"
                try:
                    with open(file_path, 'r') as file:
                        file.seek(last_position)
                        file_content = file.read()
                        match = re.search(r'Requests per second: (\d+(\.\d+)?)', file_content)
                        if match:
                            requests_per_second = float(match.group(1))
                            total_requests += requests_per_second
                            # Update the last read position
                            last_positions[file_name] = file.tell()
                except Exception as e:
                    print(f"Unable to read file content. Error: {e}")

            # Write the total requests to the output file
            with open(output_file_path, 'w') as output_file:
                output_file.write(f"Total Requests per second: {total_requests:.2f}")

            # Wait for 1 second before updating again
            time.sleep(1)

    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
    except PermissionError:
        print(f"Permission denied for directory: {directory_path}")
    except KeyboardInterrupt:
        print("\nScript terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the directory path
directory_path = "requests_log"
# Specify the output file path
output_file_path = os.path.join("requests_combined", "combined_output.txt")

# Write the total requests from files in the specified directory to the output file every second
write_requests_total(directory_path, output_file_path)
