import json
from utils.utils import get_commit_pr

with open("json/hugo-selected-NONSECUR.json") as f:
    data = json.load(f)

    full_data = []

    for d in data:
        pr_target_bic = get_commit_pr(d["repo_name"], d["target_matched"])
        pr_closest_bic = get_commit_pr(d["repo_name"], d["closest_matched"])

        d["pr_target_bic"] = pr_target_bic
        d["pr_closest_bic"] = pr_closest_bic

        full_data.append(d)

    with open("json/hugo-selected-NONSECUR-PR.json", "w") as f:
        json.dump(full_data, f, indent=4)
        