import json

def split_json_file(input_file, output_prefix, max_items_per_file=10):
    with open(input_file, 'r') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("The input file does not contain a JSON list.")

    chunks = [data[i:i + max_items_per_file] for i in range(0, len(data), max_items_per_file)]

    for idx, chunk in enumerate(chunks):
        output_file = f"{output_prefix}_{idx + 1}.json"
        with open(output_file, 'w') as f:
            json.dump(chunk, f, indent=4)
        print(f"File {output_file} created with {len(chunk)} items.")
              
input_file = ''  
output_prefix = ''  
split_json_file(input_file, output_prefix)
