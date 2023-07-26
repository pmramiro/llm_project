# Use a base image with Python installed
FROM python:3.9-slim

# Set the working directory inside the container to "llm-app"
WORKDIR /llm-app

# Copy only the requirements.txt file to the container
COPY requirements.txt /llm-app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the directories to the container
COPY src /llm-app/src
COPY data /llm-app/src

# Copy the source files to the container
COPY generate_patents.py /llm-app
COPY process_patents.py /llm-app
COPY generate_patent_summary.py /llm-app
COPY llm_api_call.py /llm-app
COPY entrypoint.sh /llm-app

# Set execute permissions for the entrypoint script
RUN chmod +x /llm-app/entrypoint.sh

# Set the default command to run the entrypoint.sh script
CMD ["/llm-app/entrypoint.sh"]