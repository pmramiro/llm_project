import os
import re
import argparse

from src.patent_processing import extract_sections, save_to_json


def process_patents(input_dir: str, output_dir: str, num_patents: int) -> None:
    """
    Processes patents, extracts relevant sections from multiple XML files, and saves them to JSON files.

    Parameters:
        input_dir (str): The directory path containing the XML files.
        output_dir (str): The directory path where JSON files will be saved.
        num_patents (int): The number of patents to process (optional).

    Returns:
        None
    """

    # Get the list of xml files in the input directory
    patent_files = [file_name for file_name in os.listdir(input_dir) if file_name.endswith(".xml")]
    patent_files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    # Initialize a counter to keep track of processed patents
    patent_count = 0

    # Loop through the files in the input directory
    for file_name in patent_files:
        # Check if the maximum number of patents to process has been reached
        if patent_count >= num_patents:
            break

        # Get the full paths of the XML and corresponding JSON files
        xml_file_path = os.path.join(input_dir, file_name)
        json_file_name = os.path.splitext(file_name)[0] + ".json"
        json_file_path = os.path.join(output_dir, json_file_name)

        # Extract relevant sections from the XML file
        extracted_data = extract_sections(xml_file_path)

        # If data was successfully extracted, save it to a JSON file
        if extracted_data:
            # Create the output directory if it doesn't exist
            os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

            # Save the data to a JSON file
            save_to_json(extracted_data, json_file_path)

            # Increment the patent count
            patent_count += 1

    # Print a message indicating that the data was saved
    print(f"Data from {num_patents} patents saved to {num_patents} JSON files:", output_dir)


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process patents and extract relevant sections.")
    parser.add_argument("--num_patents", type=int, default=100, help="Number of patents to process. If not provided, the default value is 100.")

    args = parser.parse_args()

    # Define input and output directories here
    input_directory = "data/patents_raw"
    output_directory = "data/patents_processed"

    # Process patents with the given number of patents to process
    process_patents(input_directory, output_directory, num_patents=args.num_patents)
