import openai

# Set up API credentials
api_key = "1bfdb8caf54c4aabb74538a77b67b5b5"
openai.api_key = api_key

# Specify the API endpoint
api_endpoint = "https://hiring-openai-service.openai.azure.com/"
openai.api_base = api_endpoint

# Specify the could environment
openai.api_type = 'azure'
openai.api_version = '2023-05-15'  # this may change in the future

# Read the content of the .txt file
file_path = "data/patents_summary/patent_710.txt"
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
extracted_info = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()

# Post-process and handle the extracted information as needed
print(text_prompt+extracted_info)
