import requests
import json
from pydriller import Git, Repository
import os
import logging
import re

API_TOKENS = [
    os.getenv('TOKEN_1'),
    os.getenv('TOKEN_2'),
    os.getenv('TOKEN_3')
]

token_index = 0

def get_headers():
    token = get_valid_token()
    return {'Authorization': f'token {token}'}

def get_rate_limit(token):
    headers = {'Authorization': f'token {token}'}
    response = requests.get('https://api.github.com/rate_limit', headers=headers)
    return response.json()

def get_valid_token():
    global token_index
    token = API_TOKENS[token_index]
    rate_limit = get_rate_limit(token)
    remaining = rate_limit['rate']['remaining']
    if remaining <= 0:
        token_index = (token_index + 1) % len(API_TOKENS)
        token = API_TOKENS[token_index]
    return token

def check_commit_existence(repo_path, commit_hash):
    gr = Git(repo_path)
    try:
        commit = gr.get_commit(commit_hash)
    except Exception as e:
        return False
    return True

def extract_pr_number(url):
    match = re.search(r'/pull/(\d+)', url)
    if match:
        return match.group(1)
    else:
        return None

def get_pull_request_data(url, owner, repo, repo_path):
    commit_hash = ""
    # pr_number = url.split('/pull/')[1].split('/')[0]
    pr_number = extract_pr_number(url)

    if 'commits' in url:
        try:
            commit_hash = url.split('/commits/')[1]
        except:
            commit_hash = ""

    if commit_hash != "" and check_commit_existence(repo_path, commit_hash):
        return commit_hash

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 404:
        print(f"PR {pr_number} does not exist in {owner}/{repo}.")
        return None
    data = response.json()
    merge_commit = data["merge_commit_sha"]

    if not check_commit_existence(repo_path, merge_commit):
        print(f"Merge commit {merge_commit} does not exist for PR {pr_number} in {owner}/{repo}.")
        return get_commit_that_references_pr(f"{owner}/{repo}", pr_number)

    return merge_commit

def get_commit_that_references_pr(repo_path, pr_number):
    owner, name = repo_path.split("/")
    graphql_url = 'https://api.github.com/graphql'

    query3 = f'''
    {{
        repository(name: "{name}", owner: "{owner}") {{
            pullRequest(number: {pr_number}) {{
                timelineItems(itemTypes: REFERENCED_EVENT, last: 1) {{
                    nodes {{
                        ... on ReferencedEvent {{
                            commit {{
                                oid
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
    '''

    response = requests.post(graphql_url, json={'query': query3}, headers=get_headers())
    data = response.json()
    print(data)
    if data["data"]["repository"]["pullRequest"]["timelineItems"]["nodes"] == [] or data["data"]["repository"]["pullRequest"]["timelineItems"]["nodes"][0]["commit"] is None:
        return None
    return data["data"]["repository"]["pullRequest"]["timelineItems"]["nodes"][0]["commit"]["oid"]


def get_commit_pr(repo_path, commit_hash):

    if commit_hash == []:
        return None
    
    hash = commit_hash[0]

    url = f"https://api.github.com/repos/{repo_path}/commits/{hash}/pulls"
    response = requests.get(url, headers=get_headers())
    data = response.json()

    prs = []

    for pr in data:
        if pr["state"] == "closed":
            prs.append({
                "merged_at": pr["merged_at"],
                "url": pr["html_url"]
            })

    if len(prs) == 0:
        return None
    
    pr = max(prs, key=lambda x: x["merged_at"]) 
    return pr["url"]


def match_bics(bics, bics2):
    matched = []

    if bics == '-' and bics2 == '-':
        return '-'
    elif bics == '-' or bics2 == '-':
        return matched

    for bic in bics:
       if bic in bics2:
           matched.append(bic)

    return matched


def split_json_file(input_file, output_prefix, max_items_per_file=10):
    with open(input_file, 'r') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("The input file does not contain a JSON list.")

    chunks = [data[i:i + max_items_per_file] for i in range(0, len(data), max_items_per_file)]

    for idx, chunk in enumerate(chunks):
        output_file = f"{output_prefix}_{idx + 1}.json"
        with open(output_file, 'w') as f:
            json.dump(chunk, f, indent=4)
        print(f"File {output_file} created with {len(chunk)} items.")
              
def leng(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return len(data)