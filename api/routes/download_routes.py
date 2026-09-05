from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
import os

router = APIRouter()


@router.get("/download-ppt/{company}")
def download_ppt(company: str):
    clean_company = company.strip()
    ppt_path = f"app/output/presentations/{clean_company}_Placement_Report.pptx"

    if not os.path.exists(ppt_path) and os.path.exists("app/output/presentations"):
        for fname in os.listdir("app/output/presentations"):
            if fname.lower() == f"{clean_company.lower()}_placement_report.pptx":
                ppt_path = os.path.join("app/output/presentations", fname)
                break

    if not os.path.exists(ppt_path):
        return JSONResponse(
            status_code=404,
            content={
                "status": "failed",
                "message": f"PPT presentation for '{clean_company}' not found."
            }
        )

    return FileResponse(
        path=ppt_path,
        filename=os.path.basename(ppt_path),
        media_type=(
            "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    )


@router.get("/download-report/{company}")
def download_report(company: str):
    clean_company = company.strip()
    report_path = f"app/output/reports/{clean_company}_Report.txt"

    if not os.path.exists(report_path) and os.path.exists("app/output/reports"):
        for fname in os.listdir("app/output/reports"):
            if fname.lower() == f"{clean_company.lower()}_report.txt":
                report_path = os.path.join("app/output/reports", fname)
                break

    if not os.path.exists(report_path):
        return JSONResponse(
            status_code=404,
            content={
                "status": "failed",
                "message": f"Report for '{clean_company}' not found."
            }
        )

    return FileResponse(
        path=report_path,
        filename=os.path.basename(report_path),
        media_type="text/plain; charset=utf-8"
    )