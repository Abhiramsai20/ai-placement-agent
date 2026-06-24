ROADMAP_PROMPT = """
You are an expert placement mentor.

Create a preparation roadmap.

Company:
{company}

Available Days:
{days}

Research:
{research}

Return ONLY JSON.

Format:

[
    {{
        "phase":"Phase 1",
        "days":"1-15",
        "topics":[
            "Arrays",
            "Strings"
        ]
    }},
    {{
        "phase":"Phase 2",
        "days":"16-30",
        "topics":[
            "Trees",
            "Graphs"
        ]
    }},
    {{
        "phase":"Phase 3",
        "days":"31-45",
        "topics":[
            "DBMS",
            "OS"
        ]
    }},
    {{
        "phase":"Phase 4",
        "days":"46-60",
        "topics":[
            "Mock Interviews",
            "Revision"
        ]
    }}
]

Rules:

1. Prioritize important topics.
2. Include DSA topics.
3. Include CS subjects.
4. Include Mock Interviews.
5. Use all available days.
6. Create realistic preparation phases.
7. Focus on company-specific preparation.
"""