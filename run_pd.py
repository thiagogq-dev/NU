import json
from pydriller import Git, Repository
from utils.utils import match_bics
import sys

def find_pd(json_file, repo):
    with open(json_file) as f:
        data = json.load(f)
        repo_dir_name = repo.split("/")[-1]
        for d in data:
            if d["repo_name"] == repo_dir_name:
                repo_path = f"/repos_dir/{d['repo_name']}"

                # Find the buggy commits for TARGET
                bics = pd_finder(d["Target Commit SHA"], repo_path)
                d["target_inducing_commit_hash_pd"] = bics
                d["target_matched"] = match_bics(d["targetinducing_commit_hash_pyszz"], bics)

                # Find the buggy commits for CLOSEST
                bics = pd_finder(d["Closest Commit SHA"], repo_path)
                d["closest_inducing_commit_hash_pd"] = bics
                d["closest_matched"] = match_bics(d["closest_inducing_commit_hash_pyszz"], bics)

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def pd_finder(fix_commit, repo):
    gr = Git(repo)
    commit = gr.get_commit(fix_commit)
    buggy_commits = gr.get_commits_last_modified_lines(commit)

    only_hash = []

    for key, value in buggy_commits.items():
        for val in value:
            only_hash.append(val)

    only_hash = list(set(only_hash))

    return only_hash

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_pd.py <json_file>")
        sys.exit(1)

    json_file = sys.argv[1]

    with open(f"/json/tobeProcessed/{json_file}") as f:
        data = json.load(f)
        for d in data:
            repo_path = f"pyszz_v2/repos_dir/{d['repo_name']}"

            # Find the buggy commits for TARGET
            bics = pd_finder(d["Target Commit SHA"], repo_path)
            d["target_inducing_commit_hash_pd"] = bics
            d["target_matched"] = match_bics(d["targetinducing_commit_hash_pyszz"], bics)

            # Find the buggy commits for CLOSEST
            bics = pd_finder(d["Closest Commit SHA"], repo_path)
            d["closest_inducing_commit_hash_pd"] = bics
            d["closest_matched"] = match_bics(d["closest_inducing_commit_hash_pyszz"], bics)

    with open(f"/json/final_processed/{json_file}", 'w') as f:
        json.dump(data, f, indent=4)
