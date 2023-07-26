#!/bin/bash

# Ensure the correct Python interpreter is used
#!/usr/bin/env python3

# Set the number of patents to process
NUM_PATENTS=100

# Run the script to generate patent files
python3 generate_patents.py --num_patents="$NUM_PATENTS"
generate_patents_status=$?

# Run the script to process patent files
python3 process_patents.py --num_patents="$NUM_PATENTS"
process_patents_status=$?

# Run the script to summarize patent files
python3 generate_patent_summary.py --num_patents="$NUM_PATENTS"
generate_patent_summary_status=$?

# Run the script to run the LLM on patent data
python3 llm_api_call.py
llm_api_call_status=$?

# Check the status of each script
if [ $generate_patents_status -eq 0 ] && [ $process_patents_status -eq 0 ] && [ $generate_patent_summary_status -eq 0 ] && [ $llm_api_call_status -eq 0 ]; then
    echo "All scripts have been executed successfully."
else
    echo "Error: One or more scripts failed to execute."
fi