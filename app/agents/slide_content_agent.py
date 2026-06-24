from app.services.llm_service import LLMService

from app.prompts.slide_content_prompt import (
    SLIDE_CONTENT_PROMPT
)

from app.utils.slide_json_parser import (
    extract_slide_json
)


class SlideContentAgent:

    def __init__(self):

        self.llm = LLMService()

    def run(self, state):

        print(
            "\nSlide Content Agent Running..."
        )

        company = state["company"]

        research = state.get(
            "research",
            {}
        )

        profile = state.get(
            "company_profile",
            {}
        )

        roadmap = state.get(
            "roadmap",
            []
        )

        interview_experiences = state.get(
            "interview_experiences",
            []
        )

        days = state["days"]

        # Build prompt safely
        prompt = SLIDE_CONTENT_PROMPT

        prompt = prompt.replace(
            "{company}",
            str(company)
        )

        prompt = prompt.replace(
            "{profile}",
            str(profile)
        )

        prompt = prompt.replace(
            "{research}",
            str(research)
        )

        prompt = prompt.replace(
            "{roadmap}",
            str(roadmap)
        )

        prompt = prompt.replace(
            "{interview_experiences}",
            str(interview_experiences)
        )

        prompt = prompt.replace(
            "{days}",
            str(days)
        )

        print(
            "\nPROMPT CREATED SUCCESSFULLY"
        )

        response = self.llm.generate(
            prompt
        )

        print(
            "\nLLM RESPONSE RECEIVED"
        )

        try:

            slides = extract_slide_json(
                response
            )

            state["slide_content"] = (
                slides
            )

            print(
                f"Generated {len(slides)} slides"
            )

            for slide in slides:

                print(
                    f"✓ {slide.get('title')}"
                )

        except Exception as e:

            print(
                f"Slide Parse Failed: {e}"
            )

            print(
                "\nRaw Model Response:\n"
            )

            print(response)

            state["slide_content"] = []

            raise e

        return state