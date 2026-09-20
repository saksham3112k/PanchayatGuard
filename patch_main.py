import re

with open('backend/app/main.py', 'r') as f:
    content = f.read()

replacement = '''
from fastapi import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

if os.path.exists(frontend_dist):
    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404 and not request.url.path.startswith("/api"):
            return FileResponse(os.path.join(frontend_dist, "index.html"))
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
'''

# Remove the old catch-all route
content = re.sub(r'    # Catch-all route to serve index\.html for React Router.*?return FileResponse\(os\.path\.join\(frontend_dist, "index\.html"\)\)', replacement.strip(), content, flags=re.DOTALL)

with open('backend/app/main.py', 'w') as f:
    f.write(content)
