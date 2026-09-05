from app.services.llm_service import LLMService

from app.utils.json_parser import (
    extract_json
)

from app.prompts.roadmap_prompt import (
    ROADMAP_PROMPT
)


class RoadmapAgent:

    def __init__(self):

        self.llm = LLMService()

    def run(self, state):

        print(
            "\nRoadmap Agent Running..."
        )

        company = state["company"]

        days = state["days"]

        research = state["research"]

        prompt = ROADMAP_PROMPT.format(
            company=company,
            days=days,
            research=research
        )

        response = self.llm.generate(
            prompt
        )

        try:

            roadmap = extract_json(
                response
            )

            state["roadmap"] = roadmap

            print(
                f"Generated {len(roadmap)} roadmap phases"
            )

            for phase in roadmap:

                print(
                    f"✓ {phase.get('phase')}"
                )

        except Exception as e:

            print(
                f"Roadmap Parse Failed: {e}. Generating structured fallback roadmap..."
            )

            d1 = max(1, days // 4)
            d2 = max(d1 + 1, days // 2)
            d3 = max(d2 + 1, (days * 3) // 4)

            state["roadmap"] = [
                {
                    "phase": "Phase 1: Core Foundations",
                    "days": f"1-{d1}",
                    "topics": ["Arrays", "Strings", "Hashing", "Two Pointers"]
                },
                {
                    "phase": "Phase 2: Advanced Data Structures",
                    "days": f"{d1 + 1}-{d2}",
                    "topics": ["Binary Trees", "BST", "Recursion", "Backtracking"]
                },
                {
                    "phase": "Phase 3: Algorithms & Core CS",
                    "days": f"{d2 + 1}-{d3}",
                    "topics": ["Dynamic Programming", "Graphs", "DBMS", "Operating Systems"]
                },
                {
                    "phase": "Phase 4: Mock Assessments & Revision",
                    "days": f"{d3 + 1}-{days}",
                    "topics": [f"{company} OA Problems", "System Design", "Mock Interviews", "Final Review"]
                }
            ]


        return state