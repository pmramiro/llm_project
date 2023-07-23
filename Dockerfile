# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and the data folder into the container
COPY process_patent_files.py .
COPY generate_patent_files.py .
COPY data data

# Set the entrypoint to run the script
ENTRYPOINT ["python", "script.py"]