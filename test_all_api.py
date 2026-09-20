import urllib.request

endpoints = [
    "http://localhost:8000/api/dashboard/summary",
    "http://localhost:8000/api/ai-insights",
    "http://localhost:8000/api/procurement/"
]

for url in endpoints:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            print(f"{url} -> {response.status}")
    except urllib.error.HTTPError as e:
        print(f"{url} -> {e.code} (HTTPError)")
    except Exception as e:
        print(f"{url} -> {e}")
