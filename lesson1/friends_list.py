import requests
import json

client_id = input("Введите client id: ")
client_secret = input("Введите client secret: ")
code = input("Введите code: ")

req = requests.get(
    f"https://oauth.vk.com/access_token?client_id={client_id}&client_secret={client_secret}&redirect_uri=http://localhost&code={code}")

if not req.ok:
    print(f"Ошибка авторизации: {req.status_code}")
    exit(0)

data = json.loads(req.text)
access_token = data['access_token']

req = requests.get(
    f"https://api.vk.com/method/friends.get?order=hints&count=10&fields=city,domain&access_token={access_token}&v=5.102")

if not req.ok:
    print(f"Ошибка запроса данных: {req.status_code}")
    exit(0)

data = json.loads(req.text)
with open("friends.json", "w", encoding='utf-8') as f:
    json.dump(data, f)
