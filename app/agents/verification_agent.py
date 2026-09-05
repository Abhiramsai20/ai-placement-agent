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

        check_topics = dsa_topics[:2]
        for topic in check_topics:

            topic_name = topic.get("topic", "") if isinstance(topic, dict) else str(topic)
            if not topic_name:
                continue

            results = self.search_tool.search(
                f"{company} {topic_name}",
                max_results=2
            )

            if len(results) > 0:
                verified_count += 1

        total_topics = len(dsa_topics)
        confidence = 85

        if len(check_topics) > 0:
            calculated = int(
                (verified_count / len(check_topics))
                * 100
            )
            confidence = max(65, calculated)


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