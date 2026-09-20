import requests

url = "https://api.render.com/v1/owners"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer rnd_IADQemwljZhstyUBuSVEXYoUYUda"
}
response = requests.get(url, headers=headers)
print(response.status_code)
print(response.text)
