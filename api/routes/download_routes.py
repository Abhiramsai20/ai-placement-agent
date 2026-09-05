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


@router.get("/download-report/{company}")
def download_report(company: str):

    report_path = (
        f"app/output/reports/"
        f"{company}_Report.txt"
    )

    if not os.path.exists(report_path):

        return {
            "status": "failed",
            "message": "Report not found"
        }

    return FileResponse(
        path=report_path,
        filename=f"{company}_Report.txt",
        media_type="text/plain; charset=utf-8"
    )