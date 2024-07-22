import os
import json
from utils.utils import leng

def combine_json_files(input_directory, output_file):
    combined_data = []

    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(input_directory, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                combined_data.extend(data)

    with open(output_file, 'w') as outfile:
        json.dump(combined_data, outfile, indent=4)

input_directory = './json/final_processed/'
output_file = './json/hugo-selected-NONSECUR.json'

combine_json_files(input_directory, output_file)
