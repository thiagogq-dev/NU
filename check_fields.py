import json

def is_empty_or_dash(value):
    if value == [] or value == "-":
        return True
    return False

with open('./json/hugo-selected-NONSECUR-PR.json') as f:
    data = json.load(f)

for d in data:
    if d["Closed Commit SHA"] is None:
        if not is_empty_or_dash(d["closest_inducing_commit_hash_pyszz"]) and not is_empty_or_dash(d["closest_inducing_commit_hash_pd"]):
            d["inducing_commit_hash_pyszz"] = []
            d["inducing_commit_hash_pd"] = []
            d["pr_closest_bic"] = None

    if d["Target Commit SHA"] is None:
        if not is_empty_or_dash(d["target_inducing_commit_hash_pyszz"]) and not is_empty_or_dash(d["target_inducing_commit_hash_pd"]):
            d["target_inducing_commit_hash_pyszz"] = []
            d["target_inducing_commit_hash_pd"] = []
            d["pr_target_bic"] = None