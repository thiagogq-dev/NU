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

json_file = sys.argv[1]

with open(json_file) as f:
    data = json.load(f)

    commits_data = []
    length  = len(data)
    read = 0

    repo = data[0]["repo_name"]
    clone_repositories(repo)
    
    for entry in data:
        read += 1
        print(f"Read {read}/{length}")
        url = entry["URL"]
       
        owner, repo = entry["repo_name"].split("/")
        repo_path = f"repos_dir/{owner}/{repo}"

        pr_commit_sha = get_pull_request_data(url, owner, repo, repo_path)
    
        commits_data.append({
            "repo_name": entry["repo_name"],
            "CVE_ID": entry["CVE_ID"],
            "Problem_Type": entry["Problem_Type"],
            "Description": entry["Description"],
            "URL": entry["URL"],
            "Tag": entry["Tag"],
            "fix_commit_hash": pr_commit_sha
        })

        # commits_data.append({
        #     "repo_name": entry["repo_name"],
        #     "id": entry["id"],
        #     "repo_id": entry["repo_id"],
        #     "terms_vulnerability": entry["terms_vulnerability"],
        #     "url": entry["url"],
        #     "fix_commit_hash": pr_commit_sha
        # })
        
    os.system("rm -rf repos_dir/*")
    new_file = json_file.split("/")[-1].split(".")[0]
    output_file = f"./json/with_fix_commits/{new_file}.json"
    print(f"Writing to {output_file}")
    with open(output_file, "w") as f:
        json.dump(commits_data, f, indent=4)
