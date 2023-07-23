import openai

# Set up API credentials
api_key = "1bfdb8caf54c4aabb74538a77b67b5b5"
openai.api_key = api_key

# Read the content of the .txt file
file_path = "data/patents_summary/patent_1.txt"
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
    max_tokens=100,  # Set the desired response length
)

# Extract relevant information from the response
extracted_info = response['choices'][0]['text']

# Post-process and handle the extracted information as needed
print(extracted_info)
