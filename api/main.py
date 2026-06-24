from fastapi import FastAPI

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

app.include_router(
    ppt_router
)

app.include_router(
    download_router
)


@app.get("/")
def home():

    return {
        "message":
        "AI Placement Research Agent Running"
    }