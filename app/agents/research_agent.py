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
            f"{company} online assessment pattern coding DSA questions",
            f"{company} technical interview rounds syllabus preparation tips"
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
                f"Research Parse Failed: {e}. Populating structured fallback..."
            )

            state["research"] = {
                "company": company,
                "overview": f"{company} is a major technology organization with a competitive recruitment process.",
                "oa_pattern": "70-90 minutes duration, 2-3 coding problems on data structures and algorithms.",
                "interview_rounds": "1. Online Assessment -> 2. Technical Coding (DSA) -> 3. System Design -> 4. HR Behavioral",
                "salary_range": "Competitive market package for software engineering positions",
                "dsa_topics": [
                    {"topic": "Arrays & Strings", "importance": "High", "questions": ["Two Sum", "Sliding Window Maximum"]},
                    {"topic": "Trees & Graphs", "importance": "High", "questions": ["Binary Tree Traversals", "Shortest Path"]},
                    {"topic": "Dynamic Programming", "importance": "High", "questions": ["Subsequences", "Coin Change"]}
                ],
                "cs_subjects": [
                    {"subject": "DBMS", "important_topics": ["Normalization", "Indexing", "ACID Properties"]},
                    {"subject": "Operating Systems", "important_topics": ["Process Scheduling", "Deadlocks", "Virtual Memory"]},
                    {"subject": "Computer Networks", "important_topics": ["TCP/IP", "HTTP/HTTPS", "OSI Model"]}
                ],
                "preparation_tips": [
                    f"Focus on top tagged {company} coding questions",
                    "Communicate code design clearly and verify edge cases",
                    "Master core CS concepts and discuss real-world trade-offs"
                ],
                "raw_response": response
            }

            state["sources"] = all_results


        return state