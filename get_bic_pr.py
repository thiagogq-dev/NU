import json
from utils.utils import get_commit_pr

with open("json/hugo-selected-NONSECUR.json") as f:
    data = json.load(f)
    full_data = []

    for d in data:
        pr_target_bic = get_commit_pr(d["repo_name"], d["target_matched"])
        pr_closest_bic = get_commit_pr(d["repo_name"], d["closest_matched"])

        if pr_target_bic is None and d["target_matched"] != []:
            pr_target_bic = f"https://github.com/{d['repo_name']}/commit/{d['target_matched'][0]}"
        if pr_closest_bic is None and d["closest_matched"] != []:
            pr_closest_bic = f"https://github.com/{d['repo_name']}/commit/{d['closest_matched'][0]}"

        d["pr_target_bic"] = pr_target_bic
        d["pr_closest_bic"] = pr_closest_bic

        full_data.append(d)

    with open("json/hugo-selected-NONSECUR.json", "w") as f:
        json.dump(full_data, f, indent=4)
        