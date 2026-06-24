from app.services.web_search import WebSearchTool


class VerificationAgent:

    def __init__(self):
        self.search_tool = WebSearchTool()

    def run(self, state):

        print("\nVerification Agent Running...")

        company = state["company"]

        research = state["research"]

        dsa_topics = research.get(
            "dsa_topics",
            []
        )

        verified_count = 0

        for topic in dsa_topics:

            results = self.search_tool.search(
                f"{company} {topic}"
            )

            if len(results) > 0:
                verified_count += 1

        total_topics = len(dsa_topics)

        confidence = 0

        if total_topics > 0:

            confidence = int(
                (verified_count / total_topics)
                * 100
            )

        state["verification"] = {
            "status": "Verified",
            "confidence": confidence,
            "verified_topics": verified_count,
            "total_topics": total_topics
        }

        print(
            f"Confidence: {confidence}%"
        )

        return state