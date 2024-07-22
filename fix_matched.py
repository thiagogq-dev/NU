import json

def is_empty_or_dash(value):
    if value == [] or value == "-":
        return True
    return False

with open('./json/hugo-selected-NONSECUR.json') as f:
    data = json.load(f)

for d in data:
    if d["closest_matched"] == []:
        if not is_empty_or_dash(d["closest_inducing_commit_hash_pyszz"]) and not is_empty_or_dash(d["closest_inducing_commit_hash_pd"]):
            d["closest_matched"] = d["closest_inducing_commit_hash_pyszz"]
        elif is_empty_or_dash(d["closest_inducing_commit_hash_pyszz"]) and not is_empty_or_dash(d["closest_inducing_commit_hash_pd"]):
            value = d["closest_inducing_commit_hash_pd"][0]
            d["closest_matched"] = [value]
        elif not is_empty_or_dash(d["closest_inducing_commit_hash_pyszz"]) and is_empty_or_dash(d["closest_inducing_commit_hash_pd"]):
            d["closest_matched"] = d["closest_inducing_commit_hash_pyszz"]

    if d["target_matched"] == []:
        if not is_empty_or_dash(d["target_inducing_commit_hash_pyszz"]) and not is_empty_or_dash(d["target_inducing_commit_hash_pd"]):
            d["target_matched"] = d["target_inducing_commit_hash_pyszz"]
        elif is_empty_or_dash(d["target_inducing_commit_hash_pyszz"]) and not is_empty_or_dash(d["target_inducing_commit_hash_pd"]):
            value = d["target_inducing_commit_hash_pd"][0]
            d["target_matched"] = [value]
        elif not is_empty_or_dash(d["target_inducing_commit_hash_pyszz"]) and is_empty_or_dash(d["target_inducing_commit_hash_pd"]):
            d["target_matched"] = d["target_inducing_commit_hash_pyszz"]

with open('./json/hugo-selected-NONSECUR.json', 'w') as f:
    json.dump(data, f, indent=4)