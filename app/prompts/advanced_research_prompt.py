ADVANCED_RESEARCH_PROMPT = """
You are a placement research expert.

Analyze all research data and create a complete placement preparation guide.

Company:
{company}

Research Data:
{research_data}

Return ONLY JSON.

Format:

{{
    "company":"{company}",

    "overview":"",

    "oa_pattern":"",

    "interview_rounds":"",

    "salary_range":"",

    "dsa_topics":[
        {{
            "topic":"Arrays",
            "importance":"High",
            "questions":[
                "Two Sum",
                "Sliding Window Maximum"
            ]
        }}
    ],

    "cs_subjects":[
        {{
            "subject":"DBMS",
            "important_topics":[
                "Normalization",
                "Indexing"
            ]
        }}
    ],

    "preparation_tips":[
        "...",
        "..."
    ]
}}
"""