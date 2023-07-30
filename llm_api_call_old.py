import os
import json
import openai

# Set up API credentials
api_key = "d06c6b0f881a496186066c83b3afda0c"
openai.api_key = api_key

# Specify the API endpoint
api_endpoint = "https://hiring-openai-service.openai.azure.com/"
openai.api_base = api_endpoint

# Specify the could environment
openai.api_type = 'azure'
openai.api_version = '2023-05-15'  # this may change in the future

# Define the patent number to be analyzed
patent_number = 710

# Define the input filename to be analyzed and output JSON filename to save results
input_filename = f"patent_{patent_number}.txt"
output_filename = f"patent_measurements_{patent_number}.json"

# Read the content of the .txt file
file_path = os.path.join("data", "patents_summary", input_filename)
with open(file_path, "r") as file:
    input_text = file.read()

# Text prompt for information extraction
text_prompt = "Find any measurements and their values in this text. I want to know what is being measured, the " \
              "value of the measurement and the units of the measurement. Return the information in a json " \
              "file:\n" + input_text

# Make API request
response = openai.Completion.create(
    engine="gpt-35-turbo",  # GPT-3.5 engine identifier
    prompt=text_prompt,
    max_tokens=200,  # Set the desired response length
)

# Extract relevant information from the response
extracted_info = response['choices'][0]['text'].replace('\\n', '\n').replace('\n', '').replace(' .', '.').strip()

# Prepare the data to be saved in JSON format
data_to_save = {
    "input_text": input_text,
    "extracted_info": extracted_info,
    "test": response['choices'][0]['text']
}

# Create the output directory if it doesn't exist
output_directory = "data/patents_measurements"
os.makedirs(output_directory, exist_ok=True)

# Save the extracted information to the JSON file
output_json_path = os.path.join(output_directory, output_filename)
with open(output_json_path, "w") as json_file:
    json.dump(data_to_save, json_file, indent=4)

print("Extraction completed. Information saved to", output_json_path)
