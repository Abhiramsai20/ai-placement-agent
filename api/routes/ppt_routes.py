import os
import subprocess
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models.request_models import PPTRequest

from app.agents.research_agent import (
    ResearchAgent
)

from app.agents.interview_experience_agent import (
    InterviewExperienceAgent
)

from app.agents.company_intelligence_agent import (
    CompanyIntelligenceAgent
)

from app.agents.verification_agent import (
    VerificationAgent
)

from app.agents.roadmap_agent import (
    RoadmapAgent
)

from app.agents.slide_content_agent import (
    SlideContentAgent
)

from app.agents.image_agent import (
    ImageAgent
)

from app.agents.report_agent import (
    ReportAgent
)

from app.agents.ppt_agent import (
    PPTAgent
)

router = APIRouter()


@router.post("/generate-ppt")
def generate_ppt(request: PPTRequest):

    company = request.company

    days = request.days

    state = {
        "company": company,
        "days": days
    }

    try:

        print(
            "\nStarting Placement Agent..."
        )

        # ======================
        # Research
        # ======================

        state = ResearchAgent().run(
            state
        )

        # ======================
        # Interview Experiences
        # ======================

        state = (
            InterviewExperienceAgent()
            .run(state)
        )

        # ======================
        # Company Intelligence
        # ======================

        state = (
            CompanyIntelligenceAgent()
            .run(state)
        )

        # ======================
        # Verification
        # ======================

        state = (
            VerificationAgent()
            .run(state)
        )

        # ======================
        # Roadmap
        # ======================

        state = (
            RoadmapAgent()
            .run(state)
        )

        # ======================
        # Slide Generation
        # ======================

        state = (
            SlideContentAgent()
            .run(state)
        )

        # ======================
        # Images
        # ======================

        state = (
            ImageAgent()
            .run(state)
        )

        # ======================
        # Report
        # ======================

        state = (
            ReportAgent()
            .run(state)
        )

        # ======================
        # Slides JSON
        # ======================

        state = (
            PPTAgent()
            .run(state)
        )

        ppt_path = f"app/output/presentations/{company}_Placement_Report.pptx"
        ppt_generated = os.path.exists(ppt_path)

        # Optional Node.js generator fallback/sync if node is available
        try:
            subprocess.run(
                [
                    "node",
                    "generate.js",
                    company
                ],
                cwd="ppt-generator",
                check=True
            )
            ppt_generated = True
        except Exception:
            pass

        return {

            "status": "success",

            "company": company,

            "days": days,

            "download_url":
                f"/download-ppt/{company}",

            "report_url":
                f"/download-report/{company}",

            "ppt_generated": ppt_generated,

            "slides_generated":
                len(
                    state.get(
                        "slide_content",
                        []
                    )
                ),

            "roadmap_phases":
                len(
                    state.get(
                        "roadmap",
                        []
                    )
                ),

            "image_results":
                len(
                    state.get(
                        "image_data",
                        []
                    )
                ),

            "interview_experiences":
                len(
                    state.get(
                        "interview_experiences",
                        []
                    )
                ),

            "roadmap": state.get("roadmap", []),

            "slide_content": state.get("slide_content", []),

            "company_profile": state.get("company_profile", {}),

            "verification": state.get("verification", {}),

            "report": state.get("report", "")
        }


    except Exception as e:

        return JSONResponse(
            status_code=500,
            content={
                "status": "failed",
                "error": str(e)
            }
        )