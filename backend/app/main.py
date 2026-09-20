from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth_router, dashboard_router, procurement_router, vendors_router, risk_router, geo_router, reports_router, grievances_router, notifications_router, audit_router, ai_insights_router, settings_router
import os
from dotenv import load_dotenv

load_dotenv()

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PanchayatGuard API", 
    description="Backend API for PanchayatGuard Procurement Intelligence Platform",
    version="1.0.0"
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(dashboard_router.router)
app.include_router(procurement_router.router)
app.include_router(vendors_router.router)
app.include_router(risk_router.router)
app.include_router(geo_router.router)
app.include_router(reports_router.router)
app.include_router(grievances_router.router)
app.include_router(notifications_router.router)
app.include_router(audit_router.router)
app.include_router(ai_insights_router.router)
app.include_router(settings_router.router)

from . import auth, models
from fastapi import Depends

@app.get("/")
def root():
    return {"message": "PanchayatGuard API is running. Access /docs for API documentation."}

@app.get("/api/admin-only")
def admin_only(current_user: models.User = Depends(auth.require_role(["Administrator"]))):
    return {"message": "Welcome Admin"}



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
