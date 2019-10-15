import requests
import json

# client_id = input("Введите client id: ")
# client_secret = input("Введите client secret: ")
# code = input("Введите code: ")

client_id = 7171524
client_secret = "s7QyKZnqC0V4FrjudsfB"
code = "ec1f1022c070964938"

req = requests.get(f"https://oauth.vk.com/access_token?client_id={client_id}&client_secret={client_secret}&redirect_uri=http://localhost&code={code}")

if not req.ok:
    print(f"Ошибка авторизации: {req.status_code}")
    exit(0)

data = json.loads(req.text)
access_token = data['access_token']

req = requests.get(f"https://api.vk.com/method/friends.get?order=hints&count=10&fields=city,domain&access_token=580d15314228a056094185e31ca59ee0da4338ed5dbe205e840c45f6b99f55b6b656b9fb434ee7b276d48&v=5.102")

if not req.ok:
    print(f"Ошибка запроса данных: {req.status_code}")
    exit(0)

data = json.loads(req.text)
with open("friends.json", "w", encoding='utf-8') as f:
    json.dump(data, f)

    print(data)