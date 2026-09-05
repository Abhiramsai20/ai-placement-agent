import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from api.routes.ppt_routes import (
    router as ppt_router
)

from api.routes.download_routes import (
    router as download_router
)


app = FastAPI(
    title="AI Placement Agent",
    version="1.0.0"
)

# Enable CORS for local and hosted frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    ppt_router
)

app.include_router(
    download_router
)

# Mount frontend static directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/")
def home():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    return {
        "message": "AI Placement Research Agent Running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Placement Agent"
    }