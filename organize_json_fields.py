import json

with open('./json/hugo-selected-NONSECUR-PR.json', 'r') as file:
    data = json.load(file)

new_order = [
    "repo_name", "Target PR", "Target Commit SHA", "target_inducing_commit_hash_pyszz",
    "target_inducing_commit_hash_pd", "target_matched", "pr_target_bic",
    "Closest PR", "Closest Commit SHA", "closest_inducing_commit_hash_pyszz",
    "closest_inducing_commit_hash_pd", "closest_matched", "pr_closest_bic",
    "Title", "Created At"
]

new_data = []
for item in data:
    reordered_item = {key: item[key] for key in new_order}
    new_data.append(reordered_item)

with open('./json/hugo-selected-NONSECUR-PR_novo.json', 'w') as file:
    json.dump(new_data, file, indent=4)
