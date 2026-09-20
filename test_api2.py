import urllib.request
import json

try:
    req = urllib.request.Request('http://localhost:8000/api/notifications')
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("Data:", data)
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print("Body:", e.read().decode())
except Exception as e:
    print("Error:", e)
