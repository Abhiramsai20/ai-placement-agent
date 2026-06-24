from app.services.web_search import WebSearchTool
from app.services.llm_service import LLMService

from app.prompts.advanced_research_prompt import (
    ADVANCED_RESEARCH_PROMPT
)

from app.utils.json_parser import extract_json


class ResearchAgent:

    def __init__(self):

        self.search_tool = WebSearchTool()
        self.llm = LLMService()

    def run(self, state):

        company = state["company"]

        print(f"\nResearching {company}...")

        queries = [
            f"{company} OA pattern",
            f"{company} DSA questions",
            f"{company} interview experience",
            f"{company} hiring process",
            f"{company} salary package",
            f"{company} preparation tips"
        ]

        all_results = []

        for query in queries:

            print(f"Searching: {query}")

            results = self.search_tool.search(
                query,
                max_results=5
            )

            all_results.extend(results)

        prompt = ADVANCED_RESEARCH_PROMPT.format(
            company=company,
            research_data=all_results
        )

        response = self.llm.generate(prompt)

        try:

            research_data = extract_json(
                response
            )

            state["research"] = (
                research_data
            )

            state["sources"] = all_results

            print(
                "Research Completed"
            )

        except Exception as e:

            print(
                f"Research Parse Failed: {e}"
            )

            state["research"] = {
                "raw_response": response
            }

            state["sources"] = all_results

        return state