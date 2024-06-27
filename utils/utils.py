import requests
import json

API_TOKENS = [
    "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",
    "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",
    "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"
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

def check_commit_existence(owner, repo, commit_hash):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_hash}"
    response = requests.get(url, headers=get_headers())

    if response.status_code == 422:
        return False

    return True

def get_pull_request_data(pr_number, owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=get_headers())
    data = response.json()
    print(data)
    merge_commit = data["merge_commit_sha"]

    if not check_commit_existence(owner, repo, merge_commit):
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
    if data["data"]["repository"]["pullRequest"]["timelineItems"]["nodes"] == []:
        return None
    return data["data"]["repository"]["pullRequest"]["timelineItems"]["nodes"][0]["commit"]["oid"]


def get_commit_pr(repo_path, commit_hash):
    url = f"https://api.github.com/repos/{repo_path}/commits/{commit_hash}/pulls"
    response = requests.get(url, headers=get_headers())
    data = response.json()

    prs = []

    for pr in data:
        if pr["state"] == "closed":
            prs.append({
                "merged_at": pr["merged_at"],
                "merge_commit_sha": pr["merge_commit_sha"]
            })

    if len(prs) == 0:
        return None
    
    pr = max(prs, key=lambda x: x["merged_at"]) 
    return pr["merge_commit_sha"]


def match_bics(bics, bics2):
    matched = []

    for bic in bics:
       if bic in bics2:
           matched.append(bic)

    return matched


def split_json_file(input_file, output_prefix, max_items_per_file=100):
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
              