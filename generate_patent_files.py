#!/usr/bin/env python3
import os
import argparse

from src.patent_generation import save_text_to_file, find_occurrence_positions


def extract_patents(search_str: str, input_file: str, output_dir: str, n_patents: int) -> None:
    """
    Extract patents between occurrences of the search string in the input file.

    Args:
        search_str (str): The search string to find in the input file.
        input_file (str): The path to the input file.
        output_dir (str): The output directory where files will be saved.
        n_patents (int): The number of patents to extract.

    Returns:
        None
    """

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the input file line by line and find the positions of the search string
    with open(input_file) as f:
        lines = f.readlines()

    occurrence_positions = find_occurrence_positions(lines, search_str)
    print(len(occurrence_positions))

    # Save text between occurrences to separate files
    for occurrence_number, start_line in enumerate(occurrence_positions, 1):
        if occurrence_number > n_patents:
            break
        end_line = occurrence_positions[occurrence_number] if occurrence_number < len(occurrence_positions) else None
        save_text_to_file(lines, start_line, end_line, occurrence_number, output_dir)

    print("Text between occurrences of the specified search string saved in", output_dir)


if __name__ == "__main__":

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extract text between occurrences of a search string in a file.")
    parser.add_argument("num_patents", type=int, default=100, help="Number of patents to extract. If not provided, the default value is 100.")

    args = parser.parse_args()

    # Define the search string, input file, and output dir
    search_string = '<?xml version="1.0" encoding="UTF-8"?>'
    input_file_with_patents = 'data/raw_download/ipg210105.xml'
    output_directory = "data/patents_raw"

    # Process patents with the given number of patents to process
    extract_patents(search_string, input_file_with_patents, output_directory, n_patents=args.num_patents)
