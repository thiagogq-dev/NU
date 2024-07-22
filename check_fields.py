import json

def is_empty_or_dash(value):
    if value == [] or value == "-":
        return True
    return False

file = './json/NVD-selected-NONSECUR-PR.json'

with open(file) as f:
    data = json.load(f)

for d in data:
    if d["Closest Commit SHA"] is None:
        if not is_empty_or_dash(d["closest_inducing_commit_hash_pyszz"]) and not is_empty_or_dash(d["closest_inducing_commit_hash_pd"]):
            d["closest_inducing_commit_hash_pyszz"] = []
            d["closest_inducing_commit_hash_pd"] = []
            d["pr_closest_bic"] = None

    if d["Target Commit SHA"] is None:
        if not is_empty_or_dash(d["target_inducing_commit_hash_pyszz"]) and not is_empty_or_dash(d["target_inducing_commit_hash_pd"]):
            d["target_inducing_commit_hash_pyszz"] = []
            d["target_inducing_commit_hash_pd"] = []
            d["pr_target_bic"] = None

with open(file, 'w') as f:
    json.dump(data, f, indent=4)