import json

with open("./hugo-selected-NONSECUR.json", 'r') as file:
    data = json.load(file)

sorted_data = sorted(data, key=lambda x: x["repo_name"])
with open("./hugo-selected-NONSECUR-sorted.json", 'w') as file:
    json.dump(sorted_data, file, indent=4)