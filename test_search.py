from app.agents.research_agent import ResearchAgent
from app.agents.verification_agent import VerificationAgent
from app.agents.roadmap_agent import RoadmapAgent
from app.agents.report_agent import ReportAgent
from app.agents.ppt_agent import PPTAgent


state = {
    "company": "Adobe",
    "days": 60
}

research_agent = ResearchAgent()
verification_agent = VerificationAgent()
roadmap_agent = RoadmapAgent()
report_agent = ReportAgent()
ppt_agent = PPTAgent()

state = research_agent.run(state)
state = verification_agent.run(state)
state = roadmap_agent.run(state)
state = report_agent.run(state)
state = ppt_agent.run(state)

print("\nPipeline Completed Successfully")

print("\nResearch:")
print(state["research"])

print("\nVerification:")
print(state["verification"])

print("\nRoadmap:")
print(state["roadmap"])

print("\nSlides:")
print(state["slides"])