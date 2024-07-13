import json
from utils.utils import get_pull_request_data
import os
import sys

def clone_repositories(repo_name):
    if not os.path.exists("repos_dir"):
        os.makedirs("repos_dir", exist_ok=True)

    os.system(f"git clone https://github.com/{repo_name}.git repos_dir/{repo_name}")

if not os.path.exists("json/with_fix_commits"):
    os.makedirs("json/with_fix_commits", exist_ok=True)

# json_file = sys.argv[1]

for file in os.listdir("json/raw_data"):
    print(f"Reading {file}")
    full_path = os.path.join("json/raw_data_v1", file)
    with open(full_path) as f:
        data = json.load(f)

        commits_data = []
        length  = len(data)
        read = 0

        repo = data[0]["repo_name"]
        clone_repositories(repo)
        
        for entry in data:
            read += 1
            print(f"Read {read}/{length}")
            target_pr_number = entry["Target PR"].rstrip("/").split("/")[-1]
            closest_pr_number = entry["Closest PR"].rstrip("/").split("/")[-1]
            
            owner, repo = entry["repo_name"].split("/")
            repo_path = f"repos_dir/{owner}/{repo}"

            target_commit_sha = get_pull_request_data(target_pr_number, owner, repo, repo_path)
            closest_commit_sha = get_pull_request_data(closest_pr_number, owner, repo, repo_path)

            commits_data.append({
                "repo_name": entry["repo_name"],
                "Target PR": entry["Target PR"],
                "Target Commit SHA": target_commit_sha,
                "Closest PR": entry["Closest PR"],
                "Closest Commit SHA": closest_commit_sha,
                "Title": entry["Title"],
                "Created At": entry["Created At"]
            })
            
        os.system("rm -rf repos_dir/*")
        new_file = full_path.split("/")[-1].split(".")[0]
        output_file = f"./json/with_fix_commits/{new_file}.json"
        print(f"Writing to {output_file}")
        with open(output_file, "w") as f:
            json.dump(commits_data, f, indent=4)

    # split_json_file("NVD-selected-NONSECUR-commits.json", "./json/with_fix_commits/NVD-selected-NONSECUR-commits")