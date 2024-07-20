import json
from pydriller import Git, Repository
from utils.utils import match_bics
import sys
import os

def clone_repositories(repo_name):
    if not os.path.exists("pyszz_v2/repos_dir"):
        os.makedirs("pyszz_v2/repos_dir", exist_ok=True)
    os.system(f"git clone https://github.com/{repo_name}.git pyszz_v2/repos_dir/{repo_name}")


def pd_finder(fix_commit, repo):
    gr = Git(repo)
    try:
        commit = gr.get_commit(fix_commit)
    except Exception as e:
        return []
    buggy_commits = gr.get_commits_last_modified_lines(commit)

    only_hash = []

    for key, value in buggy_commits.items():
        for val in value:
            only_hash.append(val)

    only_hash = list(set(only_hash))

    return only_hash

if __name__ == "__main__":
   
    for file in os.listdir("./json/processed_data/"):
        json_file = "./json/processed_data/" + file
        with open(json_file) as f:
            data = json.load(f)
            repo_name = data[0]["repo_name"]
            clone_repositories(repo_name)
            for d in data:
                repo_path = f"pyszz_v2/repos_dir/{d['repo_name']}"

                # Find the buggy commits for TARGET
                bics = pd_finder(d["Target Commit SHA"], repo_path)
                d["target_inducing_commit_hash_pd"] = bics
                d["target_matched"] = match_bics(d["target_inducing_commit_hash_pyszz"], bics)

                # Find the buggy commits for CLOSEST
                bics = pd_finder(d["Closest Commit SHA"], repo_path)
                d["closest_inducing_commit_hash_pd"] = bics
                d["closest_matched"] = match_bics(d["closest_inducing_commit_hash_pyszz"], bics)

        # remover tudo o que tem dentro de pyszz_v2/repos_dir
        os.system("rm -rf pyszz_v2/repos_dir")
        file_to_save = json_file.split("/")[-1]
        os.makedirs("json/final_processed", exist_ok=True)
        with open(f"json/final_processed/{file_to_save}", 'w') as f:
            json.dump(data, f, indent=4)
