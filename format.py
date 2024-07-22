import os
import json

    # "Closest Commit SHA": "fix_commit_hash",
chaves_para_substituir = {
    "fix_commit_hash": "Closest Commit SHA",
    "inducing_commit_hash_pyszz": "closest_inducing_commit_hash_pyszz",
}

def format(file):
    with open(file, 'r') as f:
        data = json.load(f)

    for entry in data:
        for old_key, new_key in chaves_para_substituir.items():
            if old_key in entry:
                entry[new_key] = entry.pop(old_key)

    with open(file, 'w') as file:
        json.dump(data, file, indent=4)


for file in os.listdir("./json/processed_data/"):
    format("./json/processed_data/" + file)
