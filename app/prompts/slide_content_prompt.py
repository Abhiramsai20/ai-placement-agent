SLIDE_CONTENT_PROMPT = """
You are an expert placement trainer, software engineer mentor, and campus recruitment specialist.

Company:
{company}

Company Profile:
{profile}

Research:
{research}

Interview Experiences:
{interview_experiences}

Preparation Days:
{days}

TASK:

Generate EXACTLY 10 slides for a professional placement preparation PowerPoint.

Return ONLY valid JSON.

Rules:

1. Generate EXACTLY 10 slides.
2. Every slide must contain 5-8 bullet points.
3. Content must be specific to {company}.
4. Include actual preparation guidance.
5. Include DSA examples.
6. Include interview preparation strategy.
7. Include a week-wise roadmap.
8. Do not return explanations.
9. Do not return markdown.
10. Return JSON only.

Required Slides:

1. Company Overview
2. Hiring Process
3. Online Assessment Pattern
4. Important DSA Topics
5. Important CS Subjects
6. Most Asked Interview Questions
7. Salary And Career Growth
8. {days}-Day Preparation Roadmap
9. Best Resources
10. Final Preparation Tips

JSON Format:

[
    {
        "title":"Company Overview",
        "content":[
            "Bullet 1",
            "Bullet 2",
            "Bullet 3",
            "Bullet 4",
            "Bullet 5"
        ]
    },
    {
        "title":"Hiring Process",
        "content":[
            "Bullet 1",
            "Bullet 2",
            "Bullet 3",
            "Bullet 4",
            "Bullet 5"
        ]
    },
    {
        "title":"Online Assessment Pattern",
        "content":[
            "Bullet 1",
            "Bullet 2",
            "Bullet 3",
            "Bullet 4",
            "Bullet 5"
        ]
    },
    {
        "title":"Important DSA Topics",
        "content":[
            "Arrays",
            "Strings",
            "Trees",
            "Graphs",
            "Example: Two Sum Problem",
            "Example: Level Order Traversal"
        ]
    },
    {
        "title":"Important CS Subjects",
        "content":[
            "DBMS",
            "Operating Systems",
            "Computer Networks",
            "OOP",
            "Important interview topics"
        ]
    },
    {
        "title":"Most Asked Interview Questions",
        "content":[
            "Question 1",
            "Question 2",
            "Question 3",
            "Question 4",
            "Question 5"
        ]
    },
    {
        "title":"Salary And Career Growth",
        "content":[
            "Package details",
            "Growth opportunities",
            "Promotion path",
            "Learning opportunities",
            "Benefits"
        ]
    },
    {
        "title":"Preparation Roadmap",
        "content":[
            "Week 1-2",
            "Week 3-4",
            "Week 5-6",
            "Week 7-8",
            "Mock Interviews"
        ]
    },
    {
        "title":"Best Resources",
        "content":[
            "LeetCode",
            "GeeksforGeeks",
            "NeetCode",
            "InterviewBit",
            "Company Interview Experiences"
        ]
    },
    {
        "title":"Final Preparation Tips",
        "content":[
            "Practice daily",
            "Revise CS subjects",
            "Take mock interviews",
            "Track progress",
            "Focus on weak areas"
        ]
    }
]
"""