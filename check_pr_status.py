import json
import requests
import re
import os
import sys

API_TOKENS = [
    os.getenv('TOKEN_1'),
    os.getenv('TOKEN_2'),
    os.getenv('TOKEN_3')
]

token_index = 0
attempted_tokens = 0  

def get_headers():
    return {
        'Authorization': f'token {API_TOKENS[token_index]}'
    }

def switch_token():
    global token_index
    token_index = (token_index + 1) % len(API_TOKENS)
    attempted_tokens += 1


PR_URL = 'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}'
COMMIT_PR_URL = 'https://api.github.com/repos/{owner}/{repo}/commits/{sha}/pulls'

def check_pr_status(input_file, file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    for item in data:

        owner = item['repo_name'].split('/')[0]
        repo = item['repo_name'].split('/')[1]

        # Checar PR para o campo URL (fix)
        fix_pr_url = item['URL']
        pr_number = re.search(r'pull/(\d+)', fix_pr_url).group(1)
        pr_url = PR_URL.format(owner=owner, repo=repo, pr_number=pr_number)

        while attempted_tokens < len(API_TOKENS):
            header = get_headers()
            response = requests.get(pr_url, headers=header)

            if response.status_code == 403:
                switch_token()
                header = get_headers()
                response = requests.get(pr_url, headers=header)
            else:
                break

        # header = get_headers()
        # response = requests.get(pr_url)

        # print(item['repo_name'])

        if attempted_tokens >= len(API_TOKENS):
            print('All tokens have been used')
            exit(1)

        # if response.status_code == 403:
        #     switch_token()
        #     header = get_headers()
        #     response = requests.get(pr_url, headers=header)

        # print(response.status_code)

        pr_data = response.json()

        if response.status_code == 404:
            url_status = 'not_found'
        else:
            if pr_data['merged'] == True:
                url_status = 'merged'
            else:
                url_status = pr_data['state']

        item["pr_status"] = url_status

    with open(f"json/done/{file}", 'w') as f:
        json.dump(data, f, indent=4)

        # remover input file
    os.remove(input_file)


        # # Checar PRs para o matched
        # if len(item['matched']) == 0:
        #     continue
        # commit = item['matched']
        # commit_pr_url = COMMIT_PR_URL.format(owner=owner, repo=repo, sha=commit)
        # response = requests.get(commit_pr_url)
        # commi_pr_data = response.json()
        # commit_pr_data_status = commi_pr_data[0]
        # if commit_pr_data_status['merged_at'] is not None:
        #     commit_pr_data_status = 'merged'
        # else:
        #     commit_pr_data_status = commit_pr_data_status['state']

        # print(len(commi_pr_data))

# pegar parãmetro passado élo terminal
input_file = sys.argv[1]
name_file = input_file.split('/')[-1]

check_pr_status(input_file)

# for file in os.listdir('json/raw_data/'):
#     check_pr_status(f'json/raw_data/{file}', file)

# check_pr_status('json/raw_data/1Panel-dev_1Panel.json')

