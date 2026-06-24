from typing import TypedDict


class AgentState(
    TypedDict,
    total=False
):

    company: str

    days: int

    research: dict

    company_profile: dict

    verification: dict

    roadmap: list

    report: str

    slides: list

    slide_content: list

    sources: list

    image_queries: list

    image_data: list

    interview_experiences: list

    logo_path: str