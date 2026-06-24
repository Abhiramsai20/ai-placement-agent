from app.agents.research_agent import ResearchAgent
from app.agents.verification_agent import VerificationAgent
from app.agents.roadmap_agent import RoadmapAgent


class CoordinatorAgent:

    def __init__(self):

        self.research_agent = ResearchAgent()
        self.verification_agent = VerificationAgent()
        self.roadmap_agent = RoadmapAgent()

    def run(self, state):

        print("\nCoordinator Agent Started")

        state = self.research_agent.run(state)

        state = self.verification_agent.run(state)

        state = self.roadmap_agent.run(state)

        print("\nCoordinator Agent Finished")

        return state