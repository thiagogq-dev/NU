import json
import os
from collections import defaultdict

# Carregar os dados do JSON
with open('./NVD-selected-NONSECUR.json', 'r') as file:
    data = json.load(file)

# Agrupar os dados pelo campo 'repo_name'
repos = defaultdict(list)
for item in data:
    repo_name = item['repo_name']
    repos[repo_name].append(item)

# Criar um diretório para armazenar os arquivos, se não existir
output_dir = 'json/raw_data/'
os.makedirs(output_dir, exist_ok=True)

# Salvar cada grupo em um arquivo separado
for repo_name, items in repos.items():
    # Criar um nome de arquivo válido a partir do nome do repositório
    filename = f"{repo_name.replace('/', '_')}.json"
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'w') as file:
        json.dump(items, file, indent=4)

print("Arquivos gerados com sucesso!")
