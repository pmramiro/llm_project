import os
import json
import openai

from src.text_segmentation import fixed_length_segmentation
from src.postprocessing import extract_measurements

# Read API credentials and other configurations from the config file
config_file = "config/config.json"
with open(config_file, "r") as config:
    config_data = json.load(config)
    api_key = config_data["api_key"]
    api_endpoint = config_data["api_endpoint"]
    api_type = config_data["api_type"]
    api_version = config_data["api_version"]

# Set up API credentials
openai.api_key = api_key
openai.api_base = api_endpoint

# Specify the cloud environment
openai.api_type = api_type
openai.api_version = api_version

# Define the patent number to be analyzed
patent_number = 710

# Define the input filename to be analyzed and output JSON filename to save results
input_filename = f"patent_{patent_number}.txt"
output_filename = f"patent_measurements_{patent_number}.json"

# Read the content of the input patent .txt file
file_path = os.path.join("data", "patents_summary", input_filename)
with open(file_path, "r") as file:
    input_text = file.read()

# Read the text prompt for information extraction from a separate file
prompt_file = os.path.join("prompts", "prompt_1.txt")
with open(prompt_file, "r") as prompt_file:
    text_prompt = prompt_file.read()

# Define the segment length for fixed-length text segmentation (number of characters per segment)
segment_length = 20000

# Define the overlap between consecutive segments
overlap = 0.8

# Get the segments of the long text using the function from src.text_segmentation
segments = fixed_length_segmentation(input_text, segment_length, overlap)

# Initialize the final response string
response_text = ""

# Make API request for each segment and concatenate responses
for segment in segments:
    response = openai.Completion.create(
        engine="gpt-35-turbo",  # GPT-3.5 engine identifier
        prompt=text_prompt + segment + "\nA: ",
        max_tokens=500,  # Set the desired response length for each segment
    )
    response_text += response['choices'][0]['text']

# Extract relevant information from the concatenated response
extracted_info = response_text.replace('\\n', '\n').replace('\n', '').replace(' .', '.').strip()

# Extract measurements from the LLM response and return them as a dictionary in JSON format
extracted_measurements = extract_measurements(extracted_info)

# Create the output directory if it doesn't exist
output_directory = "data/patents_measurements"
os.makedirs(output_directory, exist_ok=True)

# Save the extracted measurements to the JSON file
output_json_path = os.path.join(output_directory, output_filename)
with open(output_json_path, "w") as json_file:
    json.dump(extracted_measurements, json_file, indent=4)

print("Extraction completed. Information saved to", output_json_path)

# SAFETY: Prepare the data to be saved in JSON format
data_to_save = {
    "input_text": input_text,
    "extracted_info": extracted_info,
}

# Save the extracted information to the JSON file
output_json_path = os.path.join(output_directory, f"patent_measurements_{patent_number}_safety.json")
with open(output_json_path, "w") as json_file:
    json.dump(data_to_save, json_file, indent=4)

print("Extraction completed. Information saved to", output_json_path)
