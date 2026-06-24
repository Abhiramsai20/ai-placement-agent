from app.services.web_search import WebSearchTool


class InterviewExperienceAgent:

    def __init__(self):

        self.search_tool = WebSearchTool()

    def run(self, state):

        print(
            "\nInterview Experience Agent Running..."
        )

        company = state["company"]

        queries = [

            f"{company} interview experience",

            f"{company} OA experience",

            f"{company} placement interview questions",

            f"{company} campus placement experience"

        ]

        experiences = []

        for query in queries:

            results = self.search_tool.search(
                query,
                max_results=3
            )

            experiences.extend(
                results
            )

        state[
            "interview_experiences"
        ] = experiences

        print(
            f"Collected {len(experiences)} experiences"
        )

        return state