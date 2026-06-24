RESEARCH_PROMPT = """
Company Name: {company}

You are a placement research expert.

Analyze the search results.

Extract:

1. Most Asked DSA Topics
2. Most Asked CS Subjects
3. OA Pattern
4. Interview Rounds
5. Salary Range

Return ONLY valid JSON.

Format:

{{
  "company":"{company}",
  "dsa_topics":[
      "Arrays",
      "Trees"
  ],
  "cs_subjects":[
      "DBMS",
      "OS"
  ],
  "oa_pattern":"...",
  "interview_rounds":3,
  "salary_range":"..."
}}

Search Results:

{search_results}
"""