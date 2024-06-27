import json
import requests
from utils.utils import get_pull_request_data, split_json_file

file = "NVD-selected-NONSECUR.json"

with open(file) as f:
    data = json.load(f)

    commits_data = []
    len  = len(data)
    read = 0
    for entry in data:
        read += 1
        print(f"Read {read}/{len}")
        target_pr_number = entry["Target PR"].rstrip("/").split("/")[-1]
        closest_pr_number = entry["Closest PR"].rstrip("/").split("/")[-1]

        owner, repo = entry["repo_name"].split("/")

        target_commit_sha = get_pull_request_data(target_pr_number, owner, repo)
        closest_commit_sha = get_pull_request_data(closest_pr_number, owner, repo)

        commits_data.append({
            "repo_name": entry["repo_name"],
            "Target PR": entry["Target PR"],
            "Target Commit SHA": target_commit_sha,
            "Closest PR": entry["Closest PR"],
            "Closest Commit SHA": closest_commit_sha,
            "Title": entry["Title"],
            "Created At": entry["Created At"]
        })

        with open("NVD-selected-NONSECUR-commits.json", "w") as f:
            json.dump(commits_data, f, indent=4)

split_json_file("NVD-selected-NONSECUR-commits.json", "./raw_data/NVD-selected-NONSECUR-commits")