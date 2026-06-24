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
                f"Roadmap Parse Failed: {e}"
            )

            print(
                "\nRaw Model Response:\n"
            )

            print(response)

            state["roadmap"] = []

        return state