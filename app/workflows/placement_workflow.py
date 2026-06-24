from langgraph.graph import StateGraph, END

from app.models.state import AgentState

from app.agents.research_agent import ResearchAgent
from app.agents.verification_agent import VerificationAgent
from app.agents.roadmap_agent import RoadmapAgent


research_agent = ResearchAgent()
verification_agent = VerificationAgent()
roadmap_agent = RoadmapAgent()


def research_node(state):
    return research_agent.run(state)


def verification_node(state):
    return verification_agent.run(state)


def roadmap_node(state):
    return roadmap_agent.run(state)


graph = StateGraph(AgentState)

graph.add_node("research", research_node)
graph.add_node("verification", verification_node)
graph.add_node("roadmap", roadmap_node)

graph.set_entry_point("research")

graph.add_edge("research", "verification")
graph.add_edge("verification", "roadmap")
graph.add_edge("roadmap", END)

workflow = graph.compile()