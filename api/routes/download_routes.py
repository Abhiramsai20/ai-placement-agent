from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()


@router.get("/download-ppt/{company}")
def download_ppt(company: str):

    ppt_path = (
        f"app/output/presentations/"
        f"{company}_Placement_Report.pptx"
    )

    if not os.path.exists(ppt_path):

        return {
            "status": "failed",
            "message": "PPT not found"
        }

    return FileResponse(
        path=ppt_path,
        filename=(
            f"{company}_Placement_Report.pptx"
        ),
        media_type=(
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    )