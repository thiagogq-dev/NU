import json
import os
import sys

json_file = sys.argv[1]

if not os.path.exists("pyszz_v2/repos_dir"):
    os.makedirs("pyszz_v2/repos_dir", exist_ok=True)

if not os.path.exists(json_file):
    print(f"File {json_file} does not exist")
    sys.exit(1)

with open(json_file) as f:
    data = json.load(f)
    repo_name = data[0]["repo_name"]
    # for entry in data:
    #     repo_name = entry["repo_name"]

    #     print(f"Cloning {repo_name}")
    os.system(f"git clone https://github.com/{repo_name}.git pyszz_v2/repos_dir/{repo_name}")
