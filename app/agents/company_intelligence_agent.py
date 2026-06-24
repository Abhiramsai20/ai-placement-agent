from app.services.llm_service import LLMService

from app.utils.json_parser import (
    extract_json
)


class CompanyIntelligenceAgent:

    def __init__(self):

        self.llm = LLMService()

    def run(self, state):

        print(
            "\nCompany Intelligence Agent Running..."
        )

        company = state["company"]

        research = state.get(
            "research",
            {}
        )

        prompt = f"""
You are a placement expert.

Analyze the company and research data.

Company:
{company}

Research:
{research}

Return ONLY JSON.

Format:

{{
    "company_name":"",

    "company_type":"",

    "industry":"",

    "difficulty":"",

    "focus":"",

    "interview_style":"",

    "special_topics":[
        "",
        ""
    ],

    "preparation_strategy":[
        "",
        ""
    ]
}}

Rules:

1. Use the research data.
2. Identify company type.
3. Identify interview style.
4. Identify preparation focus.
5. Return ONLY JSON.
"""

        response = self.llm.generate(
            prompt
        )

        try:

            profile = extract_json(
                response
            )

            state["company_profile"] = (
                profile
            )

            print(
                "Company Profile Created"
            )

            print(profile)

        except Exception as e:

            print(
                f"Profile Parse Failed: {e}"
            )

            state["company_profile"] = {

                "company_name":
                    company,

                "company_type":
                    "Unknown",

                "industry":
                    "Software",

                "difficulty":
                    "Medium",

                "focus":
                    "DSA",

                "interview_style":
                    "Technical",

                "special_topics":
                    [],

                "preparation_strategy":
                    []
            }

        return state