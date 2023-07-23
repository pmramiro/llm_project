from typing import Dict


def extract_text_from_json(json_data: Dict[str, str]) -> str:
    """
    Extracts relevant text (Title, Abstract, Description, Claims) from the JSON data
    and concatenates them into a single input string.

    Parameters:
        json_data (dict): Dictionary containing patent data in JSON format.

    Returns:
        str: Concatenated input string containing relevant text from the JSON data.
    """

    title = json_data.get("Title", "")
    abstract = json_data.get("Abstract", "")
    description = json_data.get("Description", "")
    claims = json_data.get("Claims", "")

    # Concatenate relevant text into the input string
    input_string = f"{title}. {abstract}{description}{claims}\n"

    return input_string
