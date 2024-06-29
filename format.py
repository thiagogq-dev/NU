import os
import json

import json

# Defina um dicionário de substituições de chave
    # "fix_commit_hash": "Target Commit SHA",
    # "inducing_commit_hash_pyszz": "target_inducing_commit_hash_pyszz",
chaves_para_substituir = {
    "Closest Commit SHA": "fix_commit_hash",
}

def format(file):
    with open(file, 'r') as f:
        data = json.load(f)

    for entry in data:
        for old_key, new_key in chaves_para_substituir.items():
            if old_key in entry:
                entry[new_key] = entry.pop(old_key)

    # Salvar as alterações no arquivo JSON
    with open(file, 'w') as file:
        json.dump(data, file, indent=4)


for file in os.listdir("./json/toBeProcessed/"):
    format("./json/toBeProcessed/" + file)