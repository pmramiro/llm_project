# Patent Processing Application

This is a Dockerized Python application that processes patent data, extracts relevant sections from XML files, and generates summaries in text format. These summaries are sent to an LLM as an input with a prompt to extract measurements and their values. The application consists of several Python scripts for different stages of the processing pipeline.

## Table of Contents

- [Introduction](#introduction)
- [Directory Structure](#directory-structure)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Docker Build](#docker-build)
- [Running the Container](#running-the-container)
- [Output](#output)

## Introduction

The application uses Python scripts to perform the following tasks:

1. **generate_patents.py**: Extracts patents between occurrences of a specified search string in an input XML file and saves them as separate files in a specified output directory. Only patents containing the `<subclass>` field are extracted; further fields may be easily incorporated to this solution to only extract patents from specific technical fields. The number of patents to extract can be specified using the `NUM_PATENTS` environment variable. The number of patents to process can be specified using the `NUM_PATENTS` variable, which can be customized using the environment variable define in `entrypoint.sh` or passing it as an argument to the script.

2. **process_patents.py**: Processes the extracted patent files from the previous step, extracts relevant sections (Title, Abstract, Description, Claims, and DocNumber) from each JSON file, and saves the data as separate JSON files in another output directory. The number of patents to process can be specified using the `NUM_PATENTS` variable, which can be customized using the environment variable define in `entrypoint.sh` or passing it as an argument to the script.

3. **generate_patent_summary.py**: Summarizes the processed patent data from the previous step and saves the summaries as text files in another output directory. The number of files to process can be specified using the `NUM_PATENTS` environment variable. The number of patents to process can be specified using the `NUM_PATENTS` variable, which can be customized using the environment variable define in `entrypoint.sh` or passing it as an argument to the script.

4. **llm_api_call.py**: Reads the content contained in each of the summarized patent files and sends it to the LLM API with a custom prompt defined in this script. The default prompt defined for this challenge is: "Find any measurements and their values in this text. I want to know what is being measured, the value of the measurement and the units of the measurement. Return the information in a json file:"

The `entrypoint.sh` script runs the previous scripts sequencially when the Docker container is run.

## Directory Structure

The directory structure of the project is as follows:

- `src/`: This directory contains the Python scripts used for patent processing and summarization. The scripts are organized as follows:
  - `patent_extraction.py`: Contains helper functions for extracting patents between occurrences of a specified search string in an input XML file and saves the patent as separate file.
  - `patent_processing.py`: Contains helper functions for extracting text from XML elements and performing text corrections and replacements.
  - `patent_summarization.py`: Contains helper functions for summarizing the processed patent data from the previous step and save it as a single string.
- `data/`: This directory contains the input and output data for the patent processing pipeline. It includes the following subdirectories:
  - `patents_raw/`: This directory should contain the input XML files with patent data.
  - `patents_processed/`: This directory will store the JSON files with extracted patent sections (Title, Abstract, Description, Claims, and DocNumber).
  - `patents_summary/`: This directory will store the text files with summarized patent data.
  - `raw_download/`: This directory should contain the input XML file with patent data downloaded from [USPTO](https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2021/ipg210105.zip).
- `docs/`: This directory contains the one-page sketch that must be submitted in this challenge, named LLM_patent_challenge_PoC_strategy.pdf. It describes an approach for building a Proof of Concept solution to extract information on measurements and the values from patents.

- `requirements.txt`: This file lists the Python packages required to run the application. It will be used during the Docker image build to install the necessary dependencies.

- `Dockerfile`: This file contains the instructions to build the Docker image for the application. It sets up the working directory, installs required Python packages, and copies the necessary files and directories into the container.

- The scripts `generate_patents.py`, `process_patents.py`, `generate_patent_summary.py`, and `llm_api_call.py`, described in the previous section.

- `entrypoint.sh`: This shell script is the entry point for the Docker container. It runs the Python scripts for generating patents, processing patents, and summarizing patent data.

   ```bash
   llm_patent_project/
       ├── src/
       │   ├── patent_extraction.py
       │   ├── patent_processing.py
       │   └── patent_summarization.py
       ├── data/
       │   ├── patents_raw/
       │   ├── patents_processed/
       │   ├── patents_summary/
       │   └── raw_download/
       ├── docs/
       │   ├── llm_challenge.pdf
       │   └── LLM_patent_challenge_strategy.pdf
       ├── generate_patents.py
       ├── process_patents.py
       ├── generate_patent_summary.py
       ├── llm_api_call.py
       ├── requirements.txt
       ├── Dockerfile
       └── entrypoint.sh

## Prerequisites

To run this application, you will need:

- Docker installed on your system.

## Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/llm_patent_project.git

2. Navigate to the project directory:

   ```bash
   cd llm_patent_project
   
3. Download the `.zip` file to be used as part of this challenge from [USPTO](https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2021/ipg210105.zip) and put it in the folder `data/raw_download`


## Docker build

To build the Docker image, run the following command:

   ```bash
   docker build -t llm-patent-app .
   ```

## Running the Container

To run the Docker container and execute the patent processing pipeline, use the following command:

   ```bash
   docker run -v $(pwd)/data:/llm-app/data llm-patent-app
   ```

The -v option mounts the local data directory to the `/llm-app/data` directory inside the container.

## Output

The processed patent data will be saved in the `data/patents_processed/` directory, and the patent summaries will be saved in the `data/patents_summary/` directory.









