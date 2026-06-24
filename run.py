from app.agents.research_agent import ResearchAgent
from app.agents.verification_agent import VerificationAgent


state = {
    "company": "Adobe"
}

research_agent = ResearchAgent()
verification_agent = VerificationAgent()

state = research_agent.run(state)
state = verification_agent.run(state)

print("\nResearch:")
print(state["research"])

print("\nVerification:")
print(state["verification"])