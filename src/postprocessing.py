import re
from typing import Dict
import json


def extract_measurements(text: str) -> Dict[str, Dict[str, str]]:
    """
    Extract measurements from the given text returned by the LLM and return them as a dictionary in JSON format.

    Args:
        text (str): The input text containing measurement information returned by the LLM.

    Returns:
        Dict[str, Dict[str, str]]: A dictionary containing measurements with their respective details.

    Example:
        Input:
        "Measurement ID 1. Object: Table top. Variable: Length. Value: 6 cm to 8 cm. Units: cm.
        Measurement ID 2. Object: Table top. Variable: Width. Value: 20 cm to 22 cm. Units: cm."

        Output:
        {
            "Measurement ID 1": {
                "Object": "Table top",
                "Variable": "Length",
                "Value": "6 cm to 8 cm",
                "Units": "cm"
            },
            "Measurement ID 2": {
                "Object": "Table top",
                "Variable": "Width",
                "Value": "20 cm to 22 cm",
                "Units": "cm"
            }
        }
    """
    measurements = {}
    measurement_pattern = re.compile(r"Measurement ID (\d+)\. Object: (.+?)\. Variable: (.+?)\. Value: (.+?)\. Units: (.+?)\.")
    matches = measurement_pattern.findall(text)
    for match in matches:
        measurement_id = match[0]
        object_name = match[1]
        variable_name = match[2]
        value = match[3]
        units = match[4]
        measurement = {
            "Object": object_name,
            "Variable": variable_name,
            "Value": value,
            "Units": units
        }
        measurements[f"Measurement ID {measurement_id}"] = measurement
    return measurements


# Test the function with example input
# input_text = "Measurement ID 1. Object: Table top. Variable: Length. Value: 6 cm to 8 cm. Units: cm. Measurement ID 2. Object: Table top. Variable: Width. Value: 20 cm to 22 cm. Units: cm."
# input_text = "Measurement ID 1. Object: Poinsettia plant \u2018NPCW19282\u2019. Variable: Height. Value: 19 cm to 21 cm. Units: cm. Measurement ID 2. Object: Poinsettia plant \u2018NPCW19282\u2019. Variable: Width. Value: 29 cm to 31 cm. Units: cm. - No labels"

# result = extract_measurements(input_text)
# print(json.dumps(result, indent=2))
