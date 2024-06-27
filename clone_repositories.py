import json
import os
import sys

os.makedirs("repos_dir", exist_ok=True)
json_file = sys.argv[1]

with open(json_file) as f:
    data = json.load(f)
    for entry in data:
        repo_name = entry["repo_name"]
        if not os.path.exists("pyszz_v2/repo_dir"):
            os.makedirs(f"repos_dir/{repo_name}", exist_ok=True)

        os.chdir("repos_dir")
        os.system(f"git clone  git clone https://github.com/{repo_name}.git")
