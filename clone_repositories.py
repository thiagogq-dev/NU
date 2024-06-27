import json
import os
import sys

json_file = sys.argv[1]

if not os.path.exists("repos_dir"):
    os.makedirs("repos_dir", exist_ok=True)
os.chdir("repos_dir")

if not os.path.exists(json_file):
    print(f"File {json_file} does not exist")
    sys.exit(1)

with open(json_file) as f:
    data = json.load(f)
    for entry in data:
        repo_name = entry["repo_name"]

        print(f"Cloning {repo_name}")
        os.system(f"git clone  git clone https://github.com/{repo_name}.git {repo_name}")
