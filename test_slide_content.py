from app.agents.research_agent import ResearchAgent
from app.agents.slide_content_agent import SlideContentAgent


state = {
    "company": "Adobe",
    "days": 60
}

state = ResearchAgent().run(state)

state = SlideContentAgent().run(state)

print("\n")

for slide in state["slide_content"]:

    print(slide)

    print()