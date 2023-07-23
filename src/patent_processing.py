import xml.etree.ElementTree as ET
import json

from typing import Dict, Optional


def extract_sections(xml_file_path: str) -> Optional[Dict[str, str]]:
    """
    Extracts relevant sections (Title, Abstract, Description, Claims, and DocNumber) from an XML file.

    Parameters:
        xml_file_path (str): The path to the XML file.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the extracted sections.
                                  Returns None if an error occurs during extraction.
    """

    try:
        # Parse the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Initialize variables to store the sections
        title = ""
        abstract = ""
        description = ""
        claims = ""
        doc_number = ""

        # Extract doc-number within publication-reference
        app_reference_elem = root.find(".//application-reference")
        if app_reference_elem is not None:
            doc_id_elem = app_reference_elem.find(".//document-id")
            if doc_id_elem is not None:
                doc_number_elem = doc_id_elem.find(".//doc-number")
                if doc_number_elem is not None:
                    doc_number = doc_number_elem.text.strip()

        # Loop through the elements and extract the relevant sections
        for elem in root.iter():
            # Extract Title
            if elem.tag == 'invention-title':
                title = elem.text.strip()

            # Extract Abstract
            if elem.tag == 'abstract':
                abstract = elem.find('p').text.strip() if elem.find('p') is not None else ""

            # Extract Description
            if elem.tag == 'description':
                description = elem.text.strip()

            # Extract Claims
            if elem.tag == 'claims':
                for claim in elem.findall('claim'):
                    claim_text = claim.find('claim-text').text.strip() if claim.find('claim-text') is not None else ""
                    claims += claim_text + "\n"

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
