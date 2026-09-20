import requests

url = "https://api.render.com/v1/postgres"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer rnd_IADQemwljZhstyUBuSVEXYoUYUda"
}
data = {
    "name": "panchayat-db",
    "ownerId": "tea-danssjugekts73a2cdng",
    "plan": "free",
    "version": "15"
}
res = requests.post(url, headers=headers, json=data)
print("Postgres status:", res.status_code)
print("Postgres text:", res.text)
