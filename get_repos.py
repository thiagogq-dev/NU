import csv
import json

# Função para ler o arquivo CSV e converter para JSON
def csv_to_json(csv_file_path, json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            repo_name =  row["Target PR"].split("github.com/")[1]
            repo_name = repo_name.split("/pull/")[0]

            dados = {
                'repo_name': repo_name,
                'Target PR': row['Target PR'],
                'Closest PR': row['Closest PR'],
                'Title': row['Title'],
                'Created At': row['Created At'],
            }
            data.append(dados)
    
            with open(json_file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
                # json_file.write(json.dumps(dados, indent=4))

file = "NVD-selected-NONSECUR"

# Exemplo de uso
csv_to_json(f'{file}.csv', f'{file}.json')
