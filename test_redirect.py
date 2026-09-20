import urllib.request

try:
    req = urllib.request.Request('http://localhost:8000/api/ai-insights', method='GET')
    # Prevent urllib from automatically following redirects to see if we get a 307
    class NoRedirection(urllib.request.HTTPErrorProcessor):
        def http_response(self, request, response):
            return response
        https_response = http_response
    
    opener = urllib.request.build_opener(NoRedirection)
    res = opener.open(req)
    print("Status:", res.status)
    print("Location:", res.headers.get('Location'))
except urllib.error.HTTPError as e:
    print("HTTPError:", e.code)
