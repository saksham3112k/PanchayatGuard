with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add static file serving at the bottom of main.py
static_code = """
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

frontend_dist = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    # Catch-all route to serve index.html for React Router
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # Don't intercept API calls
        if full_path.startswith("api/"):
            return {"detail": "Not Found"}
        return FileResponse(os.path.join(frontend_dist, "index.html"))
"""

if "StaticFiles" not in content:
    with open('app/main.py', 'a', encoding='utf-8') as f:
        f.write("\n" + static_code)
