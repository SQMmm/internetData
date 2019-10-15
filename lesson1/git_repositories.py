import requests
import json

main_link = "https://api.github.com/"
user_name = "SQMmm"
link = f"{main_link}users/{user_name}/repos"
req = requests.get(link)

if req.ok:
    data = json.loads(req.text)
    with open("repositories.json", "w", encoding='utf-8') as f:
        json.dump(data, f)
else:
    print(f"returned status={req.status_code}")
