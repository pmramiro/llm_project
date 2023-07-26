import os
from typing import List, Optional


def save_text_to_file(lines: List[str], start_line: int, end_line: Optional[int], occurrence_number: int, output_dir: str) -> None:
    """
    Save text between occurrences of the search string to a file.

    Args:
        lines (List[str]): The list of lines in the input file.
        start_line (int): The line number where the current occurrence of the search string starts.
        end_line (Optional[int]): The line number where the next occurrence of the search string starts
            or None if it's the last occurrence.
        occurrence_number (int): The occurrence number of the search string.
        output_dir (str): The output directory where files will be saved.

    Returns:
        None: This function does not return anything.
    """

    output_file = os.path.join(output_dir, f"patent_{occurrence_number}.xml")
    with open(output_file, 'w') as output_f:
        output_f.writelines(lines[start_line:end_line])


def find_occurrence_positions(lines: List[str], search_string: str) -> List[int]:
    """
    Find the positions of the search string in the lines.

    Args:
        lines (List[str]): The list of lines in the input file.
        search_string (str): The search string to find in the lines.

    Returns:
        List[int]: A list of line numbers where the search string occurs.
    """

    occurrence_positions = []
    for i, line in enumerate(lines):
        if search_string in line:
            occurrence_positions.append(i)
    return occurrence_positions
