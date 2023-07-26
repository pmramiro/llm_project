import os
import re
import argparse
import json

from src.patent_summarization import extract_text_from_json


def summarize_patents(input_dir: str, output_dir: str, num_patents: int) -> None:
    """
    Summarizes patents from JSON files in the input directory and saves the summaries as text files in the output directory.

    Parameters:
        input_dir (str): The directory containing the input JSON files.
        output_dir (str): The directory where the output text files will be saved.
        num_patents (int): Number of files to process.

    Returns:
        None
    """

    # Get a list of all JSON files in the input directory and sort them numerically
    json_file_names = [file for file in os.listdir(input_dir) if file.endswith(".json")]
    json_file_names.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    # Process the specified number of files or all files if num_files is None or exceeds the number of files available
    num_patents = min(num_patents, len(json_file_names)) if num_patents is not None else len(json_file_names)

    for i in range(num_patents):
        file_name = json_file_names[i]

        # Create the full file path
        file_path = os.path.join(input_dir, file_name)

        with open(file_path, "r") as file:
            json_data = json.load(file)
            input_string = extract_text_from_json(json_data)

            # Generate the output .txt file name based on the input JSON file name
            output_file_name = file_name.replace(".json", ".txt")
            output_file_path = os.path.join(output_dir, output_file_name)

            # Save the input string to the corresponding .txt file
            with open(output_file_path, "w") as output_file:
                output_file.write(input_string)

    # Print a message indicating that the data was saved
    print(f"Data from {num_patents} patents saved to {num_patents} txt files:", output_dir)


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process JSON files and generate corresponding output .txt files.")
    parser.add_argument("--num_patents", type=int, default=100, help="Number of files to process. If not provided, the default value is 100.")

    args = parser.parse_args()

    # Define input and output directories here
    input_directory = "data/patents_processed"
    output_directory = "data/patents_summary"

    # Summarize patents with the given number of patents to summarize
    summarize_patents(input_directory, output_directory, num_patents=args.num_patents)
