import requests
import json

url = "https://api.render.com/v1/postgres/dpg-dantf1v40ujc73d46em0-a"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer rnd_IADQemwljZhstyUBuSVEXYoUYUda"
}
res = requests.get(url, headers=headers)
print("DB info status:", res.status_code)
print("DB info:", res.text)

# Also check connection-info
res2 = requests.get(url + "/connection-info", headers=headers)
print("Conn info:", res2.text)
