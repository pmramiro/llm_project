import xml.etree.ElementTree as ET
import json
import re

from typing import Dict, Optional


def extract_text_from_element(element: ET.Element) -> str:
    """
    Helper function to extract text from an XML element recursively.

    This function traverses through the element tree, handling nested elements,
    and returns the concatenated text content as a string.

    Parameters:
        element: The XML element from which to extract the text content.

    Returns:
        str: The text content of the XML element and its nested elements as a string.
    """

    # Initialize a list to accumulate text parts
    text_parts = []

    # Process the element's own text content
    if element.text:
        text_parts.append(element.text.strip())

    # Process the text content of nested elements
    for sub_element in element:
        sub_text = extract_text_from_element(sub_element)
        if sub_text:
            text_parts.append(sub_text)

        # Process the tail of the current sub-element
        if sub_element.tail:
            text_parts.append(sub_element.tail.strip())

    # Join the text parts using a dot and a space and then replace consecutive dots and spaces with a single dot and space
    text = ".".join(text_parts)
    text = ".".join(filter(None, text.split(".")))

    # Perform corrections and replacements
    text = correct_typos_and_replacements(text)

    return text


def correct_typos_and_replacements(text: str) -> str:
    """
    Correct common typos and perform replacements in the given text.

    Parameters:
        text (str): The text to be processed.

    Returns:
        str: The text with common typos corrected and replacements made.
    """

    # Correct common typos and perform replacements
    text = text.replace(":.", ".")
    text = re.sub(r'([A-Za-z])\.([A-Za-z])', r'\1. \2', text)
    text = text.replace(".—", ": ")
    text = text.replace("’.", "’. ")
    text = text.replace(": .", ": ")

    return text


def extract_sections(xml_file_path: str) -> Optional[Dict[str, str]]:
    """
    Extract relevant sections from an XML file containing patent information.

    This function parses the XML file, extracts the Title, Abstract, Description,
    Claims, and DocNumber, and returns them as a dictionary.

    Parameters:
        xml_file_path (str): The file path of the XML document to process.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the extracted sections
        (Title, Abstract, Description, Claims, and DocNumber) if successful,
        or None if there was an error during processing.
    """

    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Extract doc-number within publication-reference
        app_reference_elem = root.find(".//application-reference")
        doc_number = (
            app_reference_elem.find(".//document-id/doc-number").text.strip()
            if app_reference_elem is not None and app_reference_elem.find(".//document-id/doc-number") is not None
            else ""
        )

        # Extract Title, Abstract, and Description
        title = root.findtext('.//invention-title').strip()

        # Extract the full text content of the Abstract, including nested elements
        abstract_elem = root.find('.//abstract')
        abstract = extract_text_from_element(abstract_elem).strip() if abstract_elem is not None else ""

        # Extract the full text content of the Description, including nested elements
        description_elem = root.find('.//description')
        description = extract_text_from_element(description_elem).strip() if description_elem is not None else ""

        # Extract all claim texts
        claims_list = []
        for claim in root.findall('.//claims/claim'):
            for claim_text_elem in claim.findall('.//claim-text'):
                claim_text = extract_text_from_element(claim_text_elem)
                claims_list.append(claim_text.strip())

        # Join the claim texts with '\n' to create a single string
        claims = "\n".join(claims_list)

        # Create a dictionary to store the extracted sections
        extracted_data = {
            "Title": title,
            "Abstract": abstract,
            "Description": description,
            "Claims": claims,
            "DocNumber": doc_number
        }

        return extracted_data

    except Exception as e:
        print(f"Error: {e}")
        return None


def save_to_json(data: Dict[str, str], json_file_path: str) -> None:
    """
    Saves the extracted data to a JSON file.

    Parameters:
        data (Dict[str, str]): The extracted data to be saved as a dictionary.
        json_file_path (str): The path to the JSON file where data will be saved.

    Returns:
        None
    """

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
